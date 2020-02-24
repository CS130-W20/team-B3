from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from api.models import DiningHall, Swipe, Bid
from api.serializers import SwipeSerializer, BidSerializer
import datetime

# @param request Has a desired time and we return the swipes available
#                at each dining hall
# TODO: implement location filtering too
# returns a JSON of dining hall names with lowest ask and highest bid


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def get_swipes(request):
    """
    Given filters either for time or location, return the lowest price of an available swipe and how many are available.

    Args:
        request (Request): Expects either time or location filters

    Returns:
        JSON: dining halls with the lowest swipe available and total number of swipes "Hall": {"lowest": 4, "count": 3}
    """

    data = request.data
    hallData = {}
    desired_time = data.get('desired_time', None)
    if desired_time is None:
        desired_time = datetime.datetime.now().time()
    else:
        desired_time = datetime.datetime.strptime(desired_time, "%H:%M").time()
    halls = DiningHall.objects.all()
    for hall in halls:
        swipes = Swipe.objects.filter(location=hall.hall_id, status=0).order_by('price', 'swipe_id')
        swipes_filtered = []
        for swipe in swipes:
            for hours in swipe.visibility:
                if hours['start'].time() <= desired_time and hours['end'].time() >= desired_time:
                    swipes_filtered.append(swipe)
        hours = []
        for hour_range in hall.hours:
            # The hours objects will all be in Python datetime form, but if we're giving them to the UI they need to be JSON'able aka strings
            hours.append({k: v.strftime("%H:%M") for k, v in dict(hour_range).items()})
        hallData[hall.hall_id] = {'lowest': swipes_filtered[0].price if len(
            swipes_filtered) > 0 else None, 'count': len(swipes_filtered), 'hours': hours, 'picture': hall.picture}
    return Response(hallData, status=status.HTTP_200_OK)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def get_hall_stats(request):
    """
    Finds swipes and bids for a given hall at a given time.

    Args:
            request (Request): Object that contains the user specified hall_id and time.

    Returns:
            Reponse: HTML response containing the swipe counts, bid counts, lowest ask and highest bid meeting the user
                        specified criteria, or it returns an error HTML response.
    """

    data = request.data
    offerData = {}
    if 'hall_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED HALL_ID ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    desired_time = data.get('desired_time', None)
    if desired_time is None:
        desired_time = datetime.datetime.now()
    else:
        desired_time = datetime.datetime.strptime(desired_time, "%H:%M")
    swipes = Swipe.objects.filter(location=data['hall_id'], status=0).order_by('price', 'swipe_id')
    swipes_filtered = []
    for swipe in swipes:
        for hours in swipe.visibility:
            if hours['start'].time() <= desired_time.time() and hours['end'].time() >= desired_time.time():
                swipes_filtered.append(swipe)
    bids = Bid.objects.filter(location=data['hall_id'], status=0).order_by('-bid_price', 'bid_id')
    bids_filtered = []
    for bid in bids:
        if bid.desired_time is None or ((desired_time - datetime.timedelta(minutes=45)).time() <= bid.desired_time.time() and (desired_time + datetime.timedelta(minutes=45)).time() >= bid.desired_time.time()):
            bids_filtered.append(bid)
    offerData = {'swipe_count': len(swipes_filtered), 'bid_count': len(bids_filtered), 'lowest_ask': swipes_filtered[0].price if len(
        swipes_filtered) > 0 else None, 'highest_bid': bids_filtered[0].bid_price if len(bids_filtered) > 0 else None}
    return Response(offerData, status=status.HTTP_200_OK)
