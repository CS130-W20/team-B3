import os
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import DiningHall, Account, User, Swipe, Bid
from api.serializers import SwipeSerializer, BidSerializer, TransactionSerializer

from django.core.exceptions import ObjectDoesNotExist

import json
import stripe

# Base API URL
stripe_url = 'https://api.stripe.com'
stripe.api_key = os.environ.get("stripe_test_key")

@api_view(['POST'])
def make_payment(request):
    """
    A buyer begins the process of purchasing a swipe on the frontend, create a Stripe PaymentIntent
    Create  Transaction object to track the purchase

    Args:
        request (Request): specifies the price of the transaction, swipe_id, type("BID" or "ASK") and user_id

    Returns:
        JSON: an object with the client_secret for the frontend to use to complete the purchase
    """

    data = request.data
    if 'amount' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED amount ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    if 'swipe_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED swipe_id ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    if 'user_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED user_id ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    if 'type' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED type ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)

    price  = data["amount"]
    swipe  = data['swipe_id']
    sender = data["user_id"]
    type   = data["type"]

    intent = stripe.PaymentIntent.create(
      amount   = price,
      currency = 'usd',
    )
    client_secret = intent.client_secret

    res = {"client_secret": client_secret}

    # Get reciepient of money
    recipient = ""
    if type == "ASK":
        # get seller user_id
        swipe_obj = Swipe.objects.filter(swipe_id=swipe)
        if len(swipe_obj) != 0:
            recipient = swipe_obj[0].seller.user_id
        else:
            return Response({'STATUS': 'swipe_id does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    # Make Transaction object
    transaction = {"sender": sender, "total": price, "details": client_secret, "recipient": recipient}
    transaction_serializer = TransactionSerializer(data=transaction)
    if transaction_serializer.is_valid():
        t = transaction_serializer.save()
    else:
        print(transaction_serializer.errors)

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

    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
          json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return Response({'STATUS': e}, status=status.HTTP_400_BAD_REQUEST)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
        print("1")
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
        print("2")
        # ... handle other event types
    else:
        # Unexpected event type
        print("3")
        return HttpResponse(status=400)

    print("hi world")


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
