from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from api.models import DiningHall, Swipe, Bid, User, Account
from api.serializers import SwipeSerializer, BidSerializer
import json
import datetime
import re
import pytz
import os
from pytz import timezone
from twilio.rest import Client

stripe_test_key = os.environ.get("stripe_test_key")
twilio_account_sid = os.environ.get("twilio_account_sid")
twilio_auth_token = os.environ.get("twilio_auth_token")

@api_view(['POST'])
@renderer_classes([JSONRenderer])
# TODO: Test location filtering
def get_best_pairing(request):
    """
    Finds all bids that match the specified swipe criteria and pairs them.

    Args:
        hall_id (string): The dining hall identifier.
        time_intervals (Datatime, optional): The desired time intervals. Defaults to None.
        desired_price (Float, optional): The desired price. Defaults to None.
        pair_type:
    Returns:
        Bid/Swipe: The paired Bid or Swipe depending on which endpoint originated the request.
    """
    data = request.data
    if 'hall_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED HALL_ID ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    time_intervals = None
    if 'time_intervals' in data:
        time_intervals = []
        for interval in data['time_intervals']:
            interval_obj = {}
            for k, v in dict(interval).items():
                interval_obj[k] = datetime.datetime.strptime(v, "%H:%M").time()
            time_intervals.append(interval_obj)
    else:
        now = datetime.datetime.now()
        time_intervals = [{'start': (now - datetime.timedelta(minutes=90)).time(),
                            'end': (now + datetime.timedelta(minutes=90)).time()}]
    desired_price = data.get('desired_price', None)
    try:
        pair_type = request.resolver_match.url_name
        overlap = None
        candidates = None
        paired = None
        best_found = None
        serializer = None
        name = None
        requester_location = None
        paired_location = None
        # Get the potential bids or swipes by filtering to only unsold ones at the given location, filtered in order of highest/lowest price respectively.
        if pair_type == 'get_bid':
            candidates = Bid.objects.filter(status=0, hall_id=data['hall_id']).order_by('-bid_price', 'bid_id')
        else:
            candidates = Swipe.objects.filter(status=0, hall_id=data['hall_id']).order_by('price', 'swipe_id')
        if 'user_id' in data:
            requester_location = Account.objects.get(user_id=data['user_id']).cur_loc # Go ahead and get the requester's location, it's okay if it's None because the distance function will handle it
            if pair_type == 'get_bid':
                candidates = candidates.exclude(buyer__user_id=data['user_id'])
            else:
                candidates = candidates.exclude(seller__user_id=data['user_id'])
        for candidate in candidates:
            if paired is not None and ((pair_type == 'get_bid' and float(paired.bid_price) > float(candidate.bid_price)) or (pair_type == 'get_swipe' and float(paired.price) < float(candidate.price))): # If on a second iteration or more, check to see if this next candidate is worse than the current best
                break # If the next potential candidate is a worse value (either lower bid price or higher swipe price), we don't care about checking location or even the interval overlaps
            # If a desired price has been specified and the highest priced bid is less than what the seller wants, we'll just create the Swipe object w/o tying the bid to it
            if desired_price is not None and ((pair_type == 'get_bid' and float(desired_price) > float(candidate.bid_price)) or (pair_type == 'get_swipe' and float(desired_price) < float(candidate.price))):
                return Response({}, status=status.HTTP_200_OK)
            for potential_hours in candidate.visibility:
                for desired_hours in time_intervals:
                    overlap_start = max(desired_hours['start'], potential_hours['start'].time())
                    overlap_end = min(desired_hours['end'], potential_hours['end'].time())
                    if overlap_start <= overlap_end: # A potential candidate, intervals line up
                        candidate_location = None
                        if requester_location is not None: # Assuming the requester has a current location tied to their account
                            candidate_user_id = candidate.buyer_id if pair_type == 'get_bid' else candidate.seller_id
                            try:
                                candidate_location = Account.objects.get(user_id=candidate_user_id).cur_loc
                            except Account.DoesNotExist:
                                candidate_location = None # It really isn't a problem if they don't have a location paired, we'll just return the max float for distance so subsequent iterations of identically priced bids/swipes will prefer those with locations
                        if paired is None or Location.distance(requester_location, candidate_location) < Location.distance(requester_location, paired_location): # Either first iteration or this candidate is closer
                            paired = candidate
                            paired_location = candidate_location # Only used if requester_location is set, since we'll only run one iteration if it's None
                            overlap = {'start': overlap_start.strftime("%H:%M"), 'end': overlap_end.strftime("%H:%M")}
            if paired is not None and requester_location is None:
                break
        if pair_type == 'get_bid':
            serializer = BidSerializer(paired)
            name = paired.buyer.name if paired is not None else name
        else:
            serializer = SwipeSerializer(paired)
            name = paired.seller.name if paired is not None else name
        return Response(dict(name=name, overlap=overlap, **serializer.data), status=status.HTTP_200_OK)
    except ObjectDoesNotExist: # Generic Django exception for if either no bids or swipes exist meeting the hall/status criteria
        return Response({}, status=status.HTTP_200_OK)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def create_and_pair(request):
    data = request.data
    if 'user_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT FOR ORIGINATING USER'}, status=status.HTTP_400_BAD_REQUEST)
    if 'hall_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED HALL_ID ARGUMENT FOR BID/SWIPE'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        pair_type = request.resolver_match.url_name
        paired = None
        paired_serializer = None
        paired_phone = None
        serializer = None
        creator_phone = Account.objects.get(user_id=data['user_id']).phone
        serial_data = {'seller': data['user_id'], 'hall_id': data['hall_id'], 'price': data.get('desired_price', None), 'visibility': data.get('time_intervals', None)}
        if pair_type == 'sell_swipe' and 'bid_id' in data:
            paired = Bid.objects.get(bid_id=data['bid_id'])
        elif pair_type == 'buy_swipe' and 'swipe_id' in data:
            paired = Swipe.objects.get(swipe_id=data['swipe_id'])
        if paired is not None:
            if data.get('desired_time', None) is None:
                return Response({'STATUS': '1', 'REASON': 'ELIGIBLE PAIRING, BUT NO SPECIFIC TIME FOR TRANSACTION GIVEN'}, status=status.HTTP_400_BAD_REQUEST)
            serial_data['status'] = '1'
            if pair_type == 'sell_swipe':
                serial_data['price'] = paired.bid_price
                paired_phone = Account.objects.get(user_id=paired.buyer_id).phone
            else:
                serial_data['price'] = paired.price
                serial_data['swipe'] = paired.swipe_id
                serial_data['desired_time'] = data['desired_time']
                paired_phone = Account.objects.get(user_id=paired.seller_id).phone
        else:
            if serial_data['visibility'] is None:
                return Response({'STATUS': '1', 'REASON': 'NO ELIGIBLE PAIRING, BUT NO DESIRED TIME RANGE TO CREATE STANDALONE OBJECT'}, status=status.HTTP_400_BAD_REQUEST)
            if serial_data['price'] is None:
                return Response({'STATUS': '1', 'REASON': 'NO ELIGIBLE PAIRING, BUT NO DESIRED PRICE TO CREATE STANDALONE OBJECT'}, status=status.HTTP_400_BAD_REQUEST)
        if pair_type == 'sell_swipe':
            serializer = SwipeSerializer(data=serial_data)
        else:
            serial_data['buyer'] = serial_data.pop('seller')
            serial_data['bid_price'] = serial_data.pop('price')
            serializer = BidSerializer(data=serial_data)
        if serializer.is_valid():
            saved = serializer.save()
            if paired is not None:
                if pair_type == 'sell_swipe':
                    paired_serializer = BidSerializer(paired, data={'status': '1', 'swipe': saved.swipe_id, 'desired_time': data['desired_time']}, partial=True)
                else:
                    paired_serializer = SwipeSerializer(paired, data={'status': '1'}, partial=True)
                if paired_serializer.is_valid():
                    paired = paired_serializer.save()
                else:
                    return Response({'STATUS': '1', 'REASON': 'PAIRED OBJECT SERIALIZER ERROR', 'ERRORS': {**paired_serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)
            twilio_client = Client(twilio_account_sid, twilio_auth_token)
            creator_phone = re.sub('[^0-9]+', '', creator_phone)
            creator_msg = "This is SwipeX, letting you know that while we haven't found a " + ("seller" if saved.__class__.__name__ == 'Bid' else "buyer") + " for your " + ("bid" if saved.__class__.__name__ == 'Bid' else "swipe sale") + " request at this time, you've been entered into the queue and will be notified when a pairing occurs. Thank you for choosing SwipeX!"
            if paired_phone is not None:
                paired_phone = re.sub('[^0-9]+', '', paired_phone)
                paired_phone_formatted = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1-", "%d" % int(paired_phone[:-1])) + paired_phone[-1]
                creator_phone_formatted = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1-", "%d" % int(creator_phone[:-1])) + creator_phone[-1]
                creator_msg = "This is SwipeX, letting you know that we were able to find and match you with a " + ("buyer for your swipe" if saved.__class__.__name__ == 'Swipe' else "seller for your bid") + " that would like to meet at *ADD TIME HERE*. You can contact them at " + paired_phone_formatted + " to coordinate more details. Thank you for choosing SwipeX!"
                paired_msg = "This is SwipeX with an update for you on your existing " + ("bid" if paired.__class__.__name__ == 'Bid' else "swipe sale") + " request. You've been paired with a " + ("seller" if paired.__class__.__name__ == 'Bid' else "buyer") + " that would like to meet at *ADD TIME HERE*. You can contact them at " + creator_phone_formatted + " to coordinate more details. Thank you for choosing SwipeX!"
                paired_phone = "+" + ("1" if len(paired_phone) == 10 else "") + paired_phone
                twilio_client.messages.create(body=paired_msg, from_='+18563065093', to=paired_phone)
            creator_phone = "+" + ("1" if len(creator_phone) == 10 else "") + creator_phone
            twilio_client.messages.create(body=creator_msg, from_='+18563065093', to=creator_phone)
            if paired is not None:
                return Response({'STATUS': '0', 'REASON': 'SWIPE/BID CREATED, PAIRED WITH COMPLEMENT'}, status=status.HTTP_200_OK)
            return Response({'STATUS': '0', 'REASON': 'SWIPE/BID CREATED, NO ELIGIBLE COMPLEMENT PAIRED'}, status=status.HTTP_200_OK)
        return Response({'STATUS': '1', 'REASON': 'ORIGINATING SERIALIZER ERROR', 'ERRORS': {**serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({'STATUS': '1', 'REASON': 'NO BID/SWIPE EXISTS WITH GIVEN ID'}, status=status.HTTP_400_BAD_REQUEST)

# @param request Has a desired time and we return the swipes available
#                at each dining hall
# TODO: implement location filtering too
# returns a JSON of dining hall names with lowest ask and highest bid
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_swipes(request):
    """
    Return swipe data for each dining hall; used to populate main page

    Args:
        request (Request): does't need inputs

    Returns:
        JSON: dining halls with the lowest swipe available and total number of swipes {"Hall": {"nBids": 1, "nSwipes": 1, "times": {"start": 17, "end": 20}, "lowest_ask": 5}}
    """

    halls_list = ["FEAST at Rieber", "De Neve", "Covel", "Bruin Plate"]
    quick_list = ["Bruin Cafe", "Cafe 1919", "Rendezvous", "The Study at Hedrick"]

    hall_data = {"halls":[], "quick":[]}
    halls = DiningHall.objects.all()

    date = datetime.datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    cur_time = date.time().hour

    for hall in halls:

        cur_id = hall.hall_id
        cur_name = hall.name

        # see if hall is currently open
        hours = hall.hours
        times = {'start': 0, 'end': 0}
        found = False

        for h in hours:
            start = h['start'].hour
            end   = h['end'].hour

            # Handle midnight being stored as a 0 and Study closing at 2 am
            end_compare = end
            if end == 0 or end == 2:
                end_compare = 24 + end

            if start <= cur_time and cur_time < end_compare:
                times['start'] = start
                times['end']   = end
                found = True
                break

            elif cur_time < start:
                times['start'] = start
                times['end']   = end

        if not found and times['end'] <= cur_time:
            times['start'] = hours[0]["start"].hour
            times['end']   = hours[0]["end"].hour

        # get stats for number of swipes and bids
        swipes = Swipe.objects.filter(status=0, hall_id=cur_id)
        nSwipes  = swipes.count()

        bids = Bid.objects.filter(status=0, hall_id=cur_id)
        nBids = bids.count()

        # lowest ask
        lowest = 0
        sorted_swipes = swipes.order_by('price')
        if len(sorted_swipes) >= 1:
            lowest = sorted_swipes[0].price

        # insert cur_hall into hall_data
        cur_hall = {"hall_id": cur_id, "picture_link": hall.picture, "name": cur_name, "nBids": nBids, "nSwipes": nSwipes, "times": times, "lowest_ask": lowest}
        if cur_name in halls_list:
            hall_data["halls"].append(cur_hall)
        elif cur_name in quick_list:
            hall_data["quick"].append(cur_hall)

    return Response(json.dumps(hall_data), status=status.HTTP_200_OK)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def get_hall_stats(request):
    """
    Finds swipes and bids for a given hall at a given time.

    Args:
            request (Request): Object that contains the user specified hall_id and time.

    Returns:
            Reponse: HTML response containing the swipe counts, bid counts, lowest ask and highest bid meeting the user
                        specified criteria, or it returns an error HTML response.
    """

    data = request.data
    offerData = {}
    if 'hall_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED HALL_ID ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    desired_time = data.get('desired_time', None)
    if desired_time is None:
        desired_time = datetime.datetime.now()
    else:
        desired_time = datetime.datetime.strptime(desired_time, "%H:%M")
    swipes = Swipe.objects.filter(hall_id=data['hall_id'], status=0).order_by('price', 'swipe_id')
    swipes_filtered = []
    for swipe in swipes:
        for hours in swipe.visibility:
            if hours['start'].time() <= desired_time.time() and hours['end'].time() >= desired_time.time():
                swipes_filtered.append(swipe)
    bids = Bid.objects.filter(hall_id=data['hall_id'], status=0).order_by('-bid_price', 'bid_id')
    bids_filtered = []
    for bid in bids:
        if bid.desired_time is None or ((desired_time - datetime.timedelta(minutes=45)).time() <= bid.desired_time.time() and (desired_time + datetime.timedelta(minutes=45)).time() >= bid.desired_time.time()):
            bids_filtered.append(bid)
    offerData = {'swipe_count': len(swipes_filtered), 'bid_count': len(bids_filtered), 'lowest_ask': swipes_filtered[0].price if len(
        swipes_filtered) > 0 else None, 'highest_bid': bids_filtered[0].bid_price if len(bids_filtered) > 0 else None}
    return Response(offerData, status=status.HTTP_200_OK)

@api_view(['POST'])
def lowestswipe_highestbid_info(request):
    """
    Get the lowest swipe price and highest bid price in a time interval

    Args:
            hall_id (string): The DiningHall identifier.
            start (int): start of the time interval
            end(int): end of the time interval

    Returns:
            {"low": (string: lowest swipe price),"high" : (string: highest bid price)}
    """
    data = request.data
    if 'hall_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED hall_id ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    if 'start' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED start ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    if 'end' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED end ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)

    info = {}

    swipe_candidates = Swipe.objects.filter(hall_id=data['hall_id'], status=0).order_by('price')
    bid_candidates = Bid.objects.filter(hall_id=data['hall_id'], status=0).order_by('bid_price')

    for i in range(int(data['start']), int(data['end']) + 1):
        info[i] = {}
        for j in range(i+1, int(data['end']) + 1):
            info[i][j] = {}
            info[i][j]["swipe"] = str(int(get_lowest_swipe(swipe_candidates, i, j)))
            info[i][j]["bid"] = str(int(get_highest_bid(bid_candidates, i, j)))

    return Response(json.dumps(info), status=status.HTTP_200_OK)

def get_lowest_swipe(swipe_candidates, start, end):
    curr_price = float("inf")
    for swipe in swipe_candidates:
        for hours in swipe.visibility:
            curr_start = str(hours['start']).split(" ")[1].split(":")[0]
            curr_end = str(hours['end']).split(" ")[1].split(":")[0]
            if max(int(curr_start), start) < min(int(curr_end), end):
                curr_price = min(curr_price, float(swipe.price))

    return 0 if curr_price == float("inf") else curr_price


def get_highest_bid(bid_candidates, start, end):
    curr_price = 0
    for bid in bid_candidates:
        for hours in bid.visibility:
            curr_start = str(hours['start']).split(" ")[1].split(":")[0]
            curr_end = str(hours['end']).split(" ")[1].split(":")[0]
            if max(int(curr_start), start) < min(int(curr_end), end):
                curr_price = max(curr_price, float(bid.bid_price))

    return curr_price
