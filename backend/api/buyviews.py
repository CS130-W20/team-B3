from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import DiningHall, Swipe, Bid
from api.serializers import BidSerializer, SwipeSerializer
import datetime

def bid_geteligibleswipe(hall_id, swipe_time=None, swipe_price=None):
	if swipe_time is None:
		swipe_time = datetime.datetime.now().time()
	else:
		swipe_time = datetime.datetime.strptime(swipe_time, "%H:%M").time()
	try:
		paired_swipe = None
		swipe_candidates = Swipe.objects.filter(status=0, hall_id=hall_id).order_by('price')
		for swipe in swipe_candidates:
			if swipe_price is not None and swipe_price < swipe.price: # If a swipe price has been specified and the lowest price swipe is more expensive than desired, there aren't any eligible swipes available at this dining hall
				return None
			for hours in swipe.hours:
				if hours['start'].time() <= data['swipe_time'].time() and hours['end'].time() >= data['swipe_time'].time(): # Assuming the desired swipe time falls within the listing's range, it's a match
					paired_swipe = swipe
			if paired_swipe is not None:
				break
		return paired_swipe
	except Swipe.DoesNotExist:
		return None

@api_view(['POST'])
def bid_placebid(request):
	data = request.data
	if 'user_id' not in data:
		return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT FOR BUYER'}, status=status.HTTP_400_BAD_REQUEST)
	if 'hall_id' not in data:
		return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED HALL_ID ARGUMENT FOR BUYER'}, status=status.HTTP_400_BAD_REQUEST)
	swipe = bid_getcheapestswipe(data['hall_id'], data.get('desired_time', None), data.get('price', None)) # Get the cheapest swipe for that hall at a given time
	if swipe is None and data.get('desired_time', None) is None:
		return Response({'STATUS': '1', 'REASON': 'NO ELIGIBLE SWIPES, BUT NO DESIRED TIME GIVEN TO CREATE BID'}, status=status.HTTP_400_BAD_REQUEST)
	bid_data = {'buyer': data['user_id'], 'bid_price': data.get('price', None), 'location': data['hall_id'], 'desired_time': data.get('desired_time', None)}
	if swipe is not None: # This performs the actual pairing between buyer and seller, because a match exists
		swipe_serializer = SwipeSerializer(swipe, data={'status': '1'}, partial=True)
		if swipe_serializer.is_valid():
			swipe = swipe_serializer.save()
			bid_data['status'] = '1'
			bid_data['swipe'] = swipe.swipe_id
			bid_data['bid_price'] = swipe.price
		else:
			return Response(swipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	if bid_data['bid_price'] is None:
		return Response({'STATUS': '1', 'REASON': 'NO ELIGIBLE SWIPES, BUT NO DESIRED PRICE GIVEN TO CREATE BID'}, status=status.HTTP_400_BAD_REQUEST)
	bid_serializer = BidSerializer(data=bid_data)
	if bid_serializer.is_valid():
		bid_serializer.save()
		return Response({'STATUS': '0'}, status=status.HTTP_200_OK)
	else:
		return Response(bid_serializer.errors, status=status.HTTP_400_BAD_REQUEST)