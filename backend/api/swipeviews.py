from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from api.models import DiningHall, Swipe, Bid, User
from api.serializers import SwipeSerializer, BidSerializer
import json
import datetime
from pytz import timezone
import pytz

@api_view(['POST'])
@renderer_classes([JSONRenderer])
# TODO: Include location filtering
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
        serializer = None
        name = None
        # Get the potential bids or swipes by filtering to only unsold ones at the given location, filtered in order of highest/lowest price respectively.
        if pair_type == 'get_bid':
            candidates = Bid.objects.filter(status=0, hall_id=data['hall_id']).order_by('-bid_price', 'bid_id')
        else:
            candidates = Swipe.objects.filter(status=0, hall_id=data['hall_id']).order_by('price', 'swipe_id')
        if 'user_id' in data:
            if pair_type == 'get_bid':
                candidates = candidates.exclude(buyer__user_id=data['user_id'])
            else:
                candidates = candidates.exclude(seller__user_id=data['user_id'])
        for candidate in candidates:
            # If a desired price has been specified and the highest priced bid is less than what the seller wants, we'll just create the Swipe object w/o tying the bid to it
            if desired_price is not None and ((pair_type == 'get_bid' and float(desired_price) > float(candidate.bid_price)) or (pair_type == 'get_swipe' and float(desired_price) < float(candidate.price))):
                return Response({}, status=status.HTTP_200_OK)
            for potential_hours in candidate.visibility:
                for desired_hours in time_intervals:
                    overlap_start = max(desired_hours['start'], potential_hours['start'].time())
                    overlap_end = min(desired_hours['end'], potential_hours['end'].time())
                    if overlap_start <= overlap_end:
                        paired = candidate
                        overlap = {'start': overlap_start.strftime("%H:%M"), 'end': overlap_end.strftime("%H:%M")}
            if paired is not None:
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
        sorted_bids = bids.order_by('bid_price')
        if len(sorted_bids) >= 1:
            lowest = sorted_bids[0].bid_price

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
