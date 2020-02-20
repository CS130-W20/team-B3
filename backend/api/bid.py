from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import DiningHall, Swipe, Bid
from api.serializers import BidSerializer, SwipeSerializer
import datetime

@api_view(['POST'])
def place_bid(request):
    data = request.data
    if 'user_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT FOR BUYER'}, status=status.HTTP_400_BAD_REQUEST)
    if 'bid_price' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED BID_PRICE ARGUMENT FOR BID'}, status=status.HTTP_400_BAD_REQUEST)

def bid_getcheapestswipe(hall_id, swipe_time=None):
	if swipe_time is None:
		swipe_time = datetime.datetime.now().time()
	else:
		swipe_time = datetime.datetime.strptime(swipe_time, "%H:%M").time()
	try:
		paired_swipe = None
		swipe_candidates = Swipe.objects.filter(status=0, hall_id=hall_id).order_by('price')
		for 
		
	except Swipe.DoesNotExist:
		return None
@api_view(['POST'])
def bid_pairlowest(request):
	data = request.data
	if 'user_id' not in data:
		return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT FOR BUYER'}, status=status.HTTP_400_BAD_REQUEST)
	if 'hall_id' not in data:
		return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT FOR BUYER'}, status=status.HTTP_400_BAD_REQUEST)
	swipe_candidates = Swipe.objects.filter(status=0, hall_id=data['hall_id']).order_by('price')
	paired_swipe = None
	for swipe in swipe_candidates:
		for hours in swipe.hours:
			if hours['start'].time() <= data['swipe_time'].time() and hours['end'].time() >= data['swipe_time'].time():
				paired_swipe = swipe
				break
		if paired_swipe is not None:
			break
	if paired_swipe is None:
		return Response({'STATUS': '1', 'REASON': 'NO SWIPE MATCHING CRITERIA AVAILABLE FOR GIVEN TIME'}, status=status.HTTP_400_BAD_REQUEST)
	swipe_serializer = SwipeSerializer(paired_swipe, data={}, partial=True)
    
		