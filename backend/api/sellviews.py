from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from api.models import DiningHall, Swipe, Bid
from api.serializers import BidSerializer, SwipeSerializer
import datetime

@api_view(['POST'])
@renderer_classes([JSONRenderer])
# TODO: Include location filtering
def swipe_geteligiblebid(request):
    """
    Finds all bids that match the specified swipe criteria and pairs them.

    Args:
        hall_id (string): The dining hall identifier.
        time_intervals (Datatime, optional): The desired time intervals. Defaults to None.
        desired_price (Float, optional): The desired price. Defaults to None.

    Returns:
        Bid: The paired bid.
    """
    data = request.data
    if 'hall_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED HALL_ID ARGUMENT FOR SELLER'}, status=status.HTTP_400_BAD_REQUEST)
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
    swipe_price = data.get('desired_price', None)
    try:
    	overlap = None
        paired_bid = None
        # Get the potential bids by only getting those that are pending, at the given location, and with the highest price
        bid_candidates = Bid.objects.filter(status=0, hall_id=data['hall_id']).order_by('-bid_price', 'bid_id')
        if 'user_id' in data:
            bid_candidates = bid_candidates.exclude(buyer__user_id=data['user_id'])
        for bid in bid_candidates:
            # If a desired price has been specified and the highest priced bid is less than what the seller wants, we'll just create the Swipe object w/o tying the bid to it
            if swipe_price is not None and float(swipe_price) > float(bid.bid_price):
                return Response({}, status=status.HTTP_200_OK)
            for bid_hours in bid.visibility:
                for swipe_hours in time_intervals:
                	overlap_start = max(swipe_hours['start'], bid_hours['start'].time())
                	overlap_end = min(swipe_hours['end'], bid_hours['end'].time())
                    if overlap_start <= overlap_end:
                        paired_bid = bid
                        overlap = {'start': overlap_start.strftime("%H:%M"), 'end': overlap_end.strftime("%H:%M")}
            if paired_bid is not None:
                break
        bid_serializer = BidSerializer(paired_bid)
        return Response(dict(name=paired_bid.buyer.name, overlap=overlap, **bid_serializer.data), status=status.HTTP_200_OK)
    except Bid.DoesNotExist:
        return Response({}, status=status.HTTP_200_OK)

# TODO: Refactor to include Twilio stuff in there
@api_view(['POST'])
def swipe_sellswipe(request):
    """
    Creates a swipe to sell.

    Args:
        request (Request): The data needed to create a new Swipe listing.

    Returns:
        Reponse: A reponse saying either the swipe was successfully created or there was an error.
    """

    data = request.data
    if 'user_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT FOR SELLER'}, status=status.HTTP_400_BAD_REQUEST)
    if 'hall_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED HALL_ID ARGUMENT FOR SELLER'}, status=status.HTTP_400_BAD_REQUEST)
    bid = None
    if 'bid_id' in data:
        try:
            bid = Bid.objects.get(bid_id=data['bid_id'])
        except Bid.DoesNotExist:
            return Response({'STATUS': '1', 'REASON': 'NO BID EXISTS WITH GIVEN BID_ID'}, status=status.HTTP_400_BAD_REQUEST)
    # Create swipe
    swipe_data = {'seller': data['user_id'], 'hall_id': data['hall_id'], 'price': data.get('desired_price', None)}
    if bid is not None:
        swipe_data['status'] = '1'
        swipe_data['price'] = bid.bid_price
        if data.get('desired_time', None) is None:
            return Response({'STATUS': '1', 'REASON': 'BID FOUND FOR PAIRING, BUT NO DESIRED TIME GIVEN TO PAIR'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        swipe_data['visibility'] = data.get('time_intervals', None)
        if swipe_data['visibility'] is None or swipe_data['price'] is None:
            return Response({'STATUS': '1', 'REASON': 'NO ELIGIBLE BIDS, BUT NO DESIRED PRICE OR TIMES GIVEN TO CREATE SWIPE'}, status=status.HTTP_400_BAD_REQUEST)

    swipe_serializer = SwipeSerializer(data=swipe_data)
    if swipe_serializer.is_valid():
        swipe = swipe_serializer.save()
        if bid is not None:
            bid_serializer = BidSerializer(bid, data={'status': '1', 'swipe': swipe.swipe_id, 'desired_time': data['desired_time']}, partial=True)
            if bid_serializer.is_valid():
                bid_serializer.save()
                # TODO: SEND TEXTS AND PAYMENT INFO TO BOTH BUYER AND SELLER
                return Response({'STATUS': '0', 'REASON': 'SWIPE CREATED, PAIRED WITH EXISTING BID'}, status=status.HTTP_200_OK)
            return Response(bid_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # TODO: SEND TEXT TO SELLER ONLY CONFIRMING SWIPE WAS CREATED
        return Response({'STATUS': '0', 'REASON': 'SWIPE CREATED, NO PAIRING'}, status=status.HTTP_200_OK)
    return Response(swipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
