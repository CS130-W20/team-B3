import os
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from api.models import DiningHall, Swipe, Bid, User
from api.serializers import BidSerializer, SwipeSerializer
import datetime
from twilio.rest import Client

stripe_test_key = os.environ.get("stripe_test_key")
twilio_account_sid = os.environ.get("twilio_account_sid")
twilio_auth_token = os.environ.get("twilio_auth_token")

@api_view(['POST'])
@renderer_classes([JSONRenderer])
# TODO: Include location filtering
def bid_geteligibleswipe(request):
    """
    Gets the cheapest Swipe object that meets the criteria for a specific Bid.

    Args:
            hall_id (string): The DiningHall identifier.
            swipe_time (DateTime, optional): The time range specified on the Bid. Defaults to None.
            swipe_price (Float, optional): The desired swipe price. Defaults to None.

    Returns:
            Swipe: A swipe that meets the criteria specified in the Bid, or None if no Swipes meet the criteria.
    """
    data = request.data
    if 'hall_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED HALL_ID ARGUMENT FOR BUYER'}, status=status.HTTP_400_BAD_REQUEST)
    swipe_price = data.get('desired_price', None)
    if 'desired_time' not in data:
        swipe_time = datetime.datetime.now().time()
    else:
        swipe_time = datetime.datetime.strptime(data['desired_time'], "%H:%M").time()
    try:
        paired_swipe = None
        swipe_candidates = Swipe.objects.filter(status=0, location=data['hall_id']).order_by('price', 'swipe_id')
        for swipe in swipe_candidates:
            # If a swipe price has been specified and the lowest price swipe is more expensive than desired, there aren't any eligible swipes available at this dining hall
            if swipe_price is not None and swipe_price < swipe.price:
                return Response({}, status=status.HTTP_200_OK)
            for hours in swipe.visibility:
                # Assuming the desired swipe time falls within the listing's range, it's a match
                if hours['start'].time() <= swipe_time and hours['end'].time() >= swipe_time:
                    paired_swipe = swipe
            if paired_swipe is not None:
                break
        swipe_serializer = SwipeSerializer(paired_swipe)
        return Response(swipe_serializer.data, status=status.HTTP_200_OK)
    except Swipe.DoesNotExist:
        return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
# TODO: Refactor for Twilio
def bid_placebid(request):
    """
    Creates a new Bid object and saves it in the database.

    Args:
            request (Request): An object containing the data needed to create a new Bid object.

    Returns:
            Response: An HTTP response indicating that a new Bid was successfully created or an HTTP error reponse
                        indicating that the Bid was not created.
    """

    data = request.data
    if 'user_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT FOR BUYER'}, status=status.HTTP_400_BAD_REQUEST)
    if 'hall_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED HALL_ID ARGUMENT FOR BUYER'}, status=status.HTTP_400_BAD_REQUEST)
    swipe = None
    if 'swipe_id' in data:
        try:
            swipe = Swipe.objects.get(swipe_id=data['swipe_id'])
        except Swipe.DoesNotExist:
            return Response({'STATUS': '1', 'REASON': 'NO SWIPE EXISTS WITH GIVEN SWIPE_ID'}, status=status.HTTP_400_BAD_REQUEST)
    if swipe is None and (data.get('desired_time', None) is None or data.get('desired_price', None) is None):
        return Response({'STATUS': '1', 'REASON': 'NO ELIGIBLE SWIPES, BUT NO DESIRED TIME OR PRICE GIVEN TO CREATE BID'}, status=status.HTTP_400_BAD_REQUEST)
    bid_data = {'buyer': data['user_id'], 'bid_price': data.get(
        'desired_price', None), 'location': data['hall_id'], 'desired_time': data.get('desired_time', None), 'bid_price': data.get('desired_price', None)}
    if swipe is not None:  # This performs the actual pairing between buyer and seller, because a match exists
        swipe_serializer = SwipeSerializer(swipe, data={'status': '1'}, partial=True)
        if swipe_serializer.is_valid():
            swipe = swipe_serializer.save()
            bid_data['status'] = '1'
            bid_data['swipe'] = swipe.swipe_id
            bid_data['bid_price'] = swipe.price
        else:
            return Response(swipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    bid_serializer = BidSerializer(data=bid_data)
    if bid_serializer.is_valid():
        bid_serializer.save()
        if swipe is not None:
            return Response({'STATUS': '0', 'REASON': 'BID CREATED, PAIRED WITH SWIPE'}, status=status.HTTP_200_OK)
        return Response({'STATUS': '0', 'REASON': 'BID CREATED, NO ELIGIBLE SWIPE PAIRED'}, status=status.HTTP_200_OK)
    else:
        return Response(bid_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def buy_listed_swipe(request): #REDUNDANT - WILL BE REMOVED SOON, ALREADY HAS BEEN REMOVED FROM URLS
    """
    Lets a buyer buy a swipe. Checks that the Swipe hasnt already been bought and then matches the buyer to the Swipe
    and saves the updated Swipe to the database.

    Args:
        request (Request): A request containing the swipe_id that is trying to be purchased at the user_id of the buyer.

    Returns:
        HTTP Response: A response indicating errors or success.
    """
    data = request.data
    if 'swipe_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED SWIPE_ID ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    elif 'user_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        swipe = Swipe.objects.get(swipe_id=data['swipe_id'])
        buyer = User.objects.get(user_id=data['user_id'])
    except Swipe.DoesNotExist:
        return Response({'STATUS': '1', 'REASON': 'SWIPE DOES NOT EXIST'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'STATUS': '1', 'REASON': 'USER DOES NOT EXIST'}, status=status.HTTP_400_BAD_REQUEST)

    if swipe.status == '0':
        swipe.status = '1'
        swipe_serializer = SwipeSerializer(swipe, data={'status': '1'}, partial=True)
        if swipe_serializer.is_valid():
            swipe_serializer.save()
            client = Client(twilio_account_sid, twilio_auth_token)
            message = client.messages.create(body=f"User {buyer.user_id} has bought your swipe!",
                                             from_='+18563065093', to='+15106486565')
        else:
            return Response(swipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'STATUS': '0', 'REASON': 'SWIPE SOLD'})
    else:
        return Response({'STATUS': '1', 'REASON': 'SWIPE ALREADY SOLD'})
