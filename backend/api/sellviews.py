from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from api.models import DiningHall, Swipe, Bid
from api.serializers import BidSerializer, SwipeSerializer
import datetime

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
