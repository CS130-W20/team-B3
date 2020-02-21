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

@api_view(['POST'])
def make_payment(request):
    """
    A buyer begins the process of purchasing a swipe on the frontend, create a Stripe PaymentIntent

    Args:
        request (Request): specifies the price of the transaction

    Returns:
        JSON: an object with the client_secret for the frontend to use to complete the purchase
    """

    data = request.data
    price = data["amount"]

    intent = stripe.PaymentIntent.create(
      amount   = price,
      currency = 'usd',
    )
    client_secret = intent.client_secret

    res = {"client_secret": client_secret}

    return Response(json.dumps(res), status=status.HTTP_200_OK)

@api_view(['GET'])
def confirm_payment(request):
    """
    Stripe has confirmed the buyer's information and the money has been transferred, so update the
    swipe object state and notify the Seller

    Args:
        request (Request): specifies the bid_id of the listing

    Returns:
        JSON: acknowledge that the backend has updated the database with {'STATUS': "OK"}
    """

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

@api_view(['POST'])
def transfer_to_seller(request):
    """
    A seller confirms that the swipe has been transferred, so we transfer the money to their account

    Args:
        request (Request): bid_id of the listing and seller_id

    Returns:
        JSON: acknowledge that the backend has updated the database with {'STATUS': "OK"}
    """

    return Response(json.dumps(res), status=status.HTTP_200_OK)
