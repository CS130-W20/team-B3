from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import DiningHall, Account, User, Swipe, Bid
from api.serializers import SwipeSerializer, BidSerializer

from django.core.exceptions import ObjectDoesNotExist

import json
import stripe

from keys import stripe_test_key

# Base API URL
stripe_url = 'https://api.stripe.com'
stripe.api_key = stripe_test_key

# init payment to us from the buyer
# input: swipe object, price
@api_view(['POST'])
def make_payment(request):

    data = request.data
    price = data["amount"]

    intent = stripe.PaymentIntent.create(
      amount   = price,
      currency = 'usd',
    )
    client_secret = intent.client_secret

    res = {"client_secret": client_secret}

    return Response(json.dumps(res), status=status.HTTP_200_OK)


# UI confirms user's card and payment worked, mark swipe as pending
# notify seller
# input: bid_id,
@api_view(['GET'])
def confirm_payment(request):

    data = request.data
    bid_id = data["bid_id"]

    try:
        bid = Bid.objects.filter(bid_id=bid_id)
    except ObjectDoesNotExist:
        return Response({'STATUS': 'bid_id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    # update bid state to pending
    # bid.

    # todo - notify seller

    return Response(json.dumps(res), status=status.HTTP_200_OK)


# Seller (and buyer?) confirms transfer of swipe, transfer funds to Seller
# mark swipes as purchased
# input: seller, swipe
@api_view(['POST'])
def transfer_to_seller(request):

    return Response(json.dumps(res), status=status.HTTP_200_OK)
