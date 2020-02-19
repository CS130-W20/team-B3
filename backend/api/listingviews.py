from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import DiningHall, Account, User, Swipe, Listing
from api.serializers import SwipeSerializer, ListingSerializer


@api_view(['POST'])
def listing_create(request):
    data = request.data
    # Need to create the Swipe first with user ID, dining hall ID, price
    if 'user_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    if 'swipe' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED SWIPE ARGUMENTS'}, status=status.HTTP_400_BAD_REQUEST)
    if 'visible_from' not in data or 'visible_to' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED TIMEFRAME ARGUMENTS'}, status=status.HTTP_400_BAD_REQUEST)
    swipe_data = data.pop('swipe')
    if type(swipe_data) == dict:
        swipe_data['seller'] = data.pop('user_id')
        swipe_serializer = SwipeSerializer(data=swipe_data)
        if swipe_serializer.is_valid():
            swipe_obj = swipe_serializer.save()
            data['swipe'] = swipe_obj.swipe_id
        else:
            return Response(swipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # The ELSE case is already handled implicitly here, for testing purposes with an existing Swipe object just make data['swipe'] the swipe ID value
    # At this stage, we have the swipe ID either from the created object or the POST itself
    listing_serializer = ListingSerializer(data=data)
    if listing_serializer.is_valid():
        listing_serializer.save()
        return Response({'STATUS': '0'}, status=status.HTTP_200_OK)
    else:
        return Response(listing_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def listing_buy(request):
    data = request.data
    status_data = data.pop('status')
    if status_data == '0':
        data['status'] = '1'
        swipe_serializer = SwipeSerializer(data=data)
        swipe_serializer.save()
        return Response({'STATUS': '0'}, status=status.HTTP_200_OK)
    else:
        swipe_serializer = SwipeSerializer(data=data)
        return Response(swipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
