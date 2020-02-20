from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import DiningHall, Swipe, Bid
from api.serializers import BidSerializer, SwipeSerializer
import datetime

def swipe_geteligiblebid(hall_id, time_intervals=None, desired_price=None):
	try:
		paired_bid = None
		bid_candidates = Bid.objects.filter(status=0, location=hall_id).order_by('-bid_price', 'bid_id') # Get the potential bids by only getting those that are pending, at the given location, and with the highest price

		for bid in bid_candidates:
			if desired_price is not None and desired_price > bid.bid_price: # If a desired price has been specified and the highest priced bid is less than what the seller wants, we'll just create the Swipe object w/o tying the bid to it
				return None
			if bid.desired_time is None: # If the buyer doesn't care when they can get swiped in, pair them
				paired_bid = bid
			else:
				if time_intervals is None: # If no time interval is given, we assume the buyer wants to sell *now* - give them a 45 minute window from the current time in either direction, see if the buyer's original desired time works with this
					now = datetime.datetime.now()
					time_intervals = [{'start': (now - datetime.timedelta(minutes=45)).time(), 'end': (now + datetime.timedelta(minutes=45)).time()}]
				for interval in time_intervals: # Loop over the time intervals, if the buyer's desired time falls in this range, it's a match
					if (bid.desired_time is not None and bid.desired_time.time() >= interval['start'] and bid.desired_time.time() <= interval['end']):
						paired_bid = bid
			if paired_bid is not None:
				break
		return paired_bid
	except Bid.DoesNotExist:
		return None

# TODO: reimplement to 
@api_view(['POST'])
def swipe_sellswipe(request):
    data = request.data
    if 'user_id' not in data:
    	return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT FOR SELLER'}, status=status.HTTP_400_BAD_REQUEST)
    if 'hall_id' not in data:
    	return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED HALL_ID ARGUMENT FOR SELLER'}, status=status.HTTP_400_BAD_REQUEST)
    time_intervals_local = None
    if 'time_intervals' in data:
    	time_intervals_local = []
    	for interval in data['time_intervals']:
    		interval_obj = {}
    		for k, v in dict(interval).items():
    			interval_obj[k] = datetime.datetime.strptime(v, "%H:%M").time()
    		time_intervals_local.append(interval_obj)
    bid = swipe_geteligiblebid(data['hall_id'], time_intervals_local, data.get('price', None))
    if bid is None and (data.get('price', None) is None or data.get('time_intervals', None) is None):
    	return Response({'STATUS': '1', 'REASON': 'NO ELIGIBLE BIDS, BUT NO DESIRED PRICE OR TIMES GIVEN TO CREATE SWIPE'})
    # Create swipe
    swipe_data = {'seller': data['user_id'], 'location': data['hall_id'], 'visibility': data['time_intervals']}
    swipe_data['price'] = bid.bid_price if (bid is not None) else data['price']
    if bid is not None:
    	swipe_data['status'] = '1'
    swipe_serializer = SwipeSerializer(data=swipe_data)
    if swipe_serializer.is_valid():
        swipe = swipe_serializer.save()
        if bid is not None:
        	bid_serializer = BidSerializer(bid, data={'status': '1', 'swipe': swipe.swipe_id}, partial=True)
        	if bid_serializer.is_valid():
        		bid_serializer.save()
        		return Response({'STATUS': '0', 'REASON': 'SWIPE CREATED, PAIRED WITH EXISTING BID'}, status=status.HTTP_200_OK)
        	else:
        		return Response(bid_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'STATUS': '0', 'REASON': 'SWIPE CREATED, NO PAIRING'}, status=status.HTTP_200_OK)
    else:
        return Response(swipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
