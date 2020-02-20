from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import DiningHall, Account, User, Swipe, Bid
from api.serializers import BidSerializer

@api_view(['POST'])
def place_bid(request):
    data = request.data
    
    if 'user_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    if 'bid_price' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED BID_PRICE ARGUMENT FOR BID'}, status=status.HTTP_400_BAD_REQUEST)
    
    bid_data = {'status': 0, 'buyer': data['user_id'], 'bid_price': data["bid_price"]}
    bid_serializer = BidSerializer(data=bid_data)
    
    if bid_serializer.is_valid():
            bid_obj = bid_serializer.save()
            bid_id = bid_obj.bid_id
            make_pair(bid_id)
            return Response({'STATUS': '0'}, status=status.HTTP_200_OK)
        else:
            return Response(bid_serializer.errors, status=status.HTTP_400_BAD_REQUEST)