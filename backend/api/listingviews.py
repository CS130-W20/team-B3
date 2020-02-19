from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import DiningHall, Account, User, Swipe, Listing, Bid
from api.serializers import SwipeSerializer, ListingSerializer, BidSerializer


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
def listing_placebid(request):
    data = request.data
    # 3 simple params, just the listing ID, the user ID of the bidder, then the price
    if 'user_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT FOR BUYER'}, status=status.HTTP_400_BAD_REQUEST)
    if 'listing_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED LISTING_ID ARGUMENT FOR LISTING'}, status=status.HTTP_400_BAD_REQUEST)
    if 'bid_price' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED BID_PRICE ARGUMENT FOR BID'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        listing_obj = Listing.objects.get(listing_id=data['listing_id']) # Attempt to get the listing associated with the given ID
    except Listing.DoesNotExist:
        return Response({'STATUS': '1', 'REASON': 'NO LISTING EXISTS WITH GIVEN LISTING_ID'}, status=status.HTTP_400_BAD_REQUEST)
    active_bidset = Bid.objects.filter(buyer=data['user_id'], swipe=listing_obj.swipe.swipe_id)
    if active_bidset.filter(status=1).exists(): # If the user has already placed a bid that's been accepted, then we shouldn't allow placing another bid
        return Response({'STATUS': '1', 'REASON': 'CONFIRMED BID ALREADY PLACED'}, status=status.HTTP_400_BAD_REQUEST)
    existing_bid = active_bidset.filter(status=0).first()
    if existing_bid is not None:
        return bid_update(existing_bid, data)
    else:
        bid_data = {'swipe': listing_obj.swipe.swipe_id, 'buyer': data['user_id'], 'bid_price': 0}
        bid_serializer = BidSerializer(data=bid_data)
        if bid_serializer.is_valid():
            bid_obj = bid_serializer.save()
            return bid_update(bid_obj, data)
        else:
            return Response(bid_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def listing_updatebid(request):
    data = request.data
    # If a given bid is still pending, allow the user to raise/lower their bidding price. Once it's locked in though (either accepted or rejected), they have to make a new bid.
    if 'bid_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED BID_ID ARGUMENT FOR BID'}, status=status.HTTP_400_BAD_REQUEST)
    if 'user_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        bid_obj = Bid.objects.get(bid_id=data['bid_id'])
    except Bid.DoesNotExist:
        return Response({'STATUS': '1', 'REASON': 'NO BID EXISTS WITH GIVEN BID_ID'})
    return bid_update(bid_obj, data)

def bid_update(bid_obj, data): # This function is only called by other API endpoints, it's not a dedicated endpoint
    if bid_obj.buyer.user_id == data['user_id']:
        if int(bid_obj.status) == 0:
            bid_status = 0 # Default to pending transaction
            bid_price = float(data.get('bid_price', bid_obj.bid_price)) # Attempt to get their new price, default to the existing bid price if they didn't specify one
            if bid_price >= float(bid_obj.swipe.price): # They hit the buy-it-now criteria
                bid_status = 1
            bid_data = {'status': bid_status, 'bid_price': bid_price}
            bid_serializer = BidSerializer(bid_obj, data=bid_data, partial=True) # Partial data update since we're only updating a couple fields
            if bid_serializer.is_valid():
                bid_serializer.save()
                if (float(bid_obj.bid_price) != bid_price and bid_price > float(bid_obj.bid_price)):
                    pass
                    # Only send a notification to the seller that a bid has been updated if they RAISE their price
                return Response({'STATUS': '0'}, status=status.HTTP_200_OK)
            else: # This is another one that should never be triggered unless the bid_price from the POST is an invalid number
                return Response(bid_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else: # Theoretically this should never be triggered because the frontend shouldn't let the user attempt to update a bid that's been finalized, but just in case...
            return Response({'STATUS': '1', 'REASON': 'BID HAS ALREADY BEEN FINALIZED'})
    else:
        return Response({'STATUS': '1', 'REASON': 'BIDDER ID MISMATCHES SUPPLIED USER'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def listing_buyergetbids(request):
    data = request.data
    # TODO: Turn this into an enum, but for now -1 gets all bids, 0 gets pending bids, 1 gets accepted, and 2 gets rejected, this matches up with BID_STATES in the Bid model
    filter_type = int(data.get('bid_filter_type', -1))
    if 'user_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    bids = None
    if filter_type == -1:
        bids = Bid.objects.filter(buyer=data['user_id'])
    elif filter_type == 0:
        bids = Bid.objects.filter(buyer=data['user_id'], status=0)
    elif filter_type == 1:
        bids = Bid.objects.filter(buyer=data['user_id'], status=1)
    elif filter_type == 2:
        bids = Bid.objects.filter(buyer=data['user_id'], status=2)
    bid_serializer = BidSerializer(bids, many=True)
    return Response(bid_serializer.data, status=status.HTTP_200_OK)