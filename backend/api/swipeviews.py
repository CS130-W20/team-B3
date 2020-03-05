from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from api.models import DiningHall, Swipe, Bid
from api.serializers import SwipeSerializer, BidSerializer
import json
import datetime
from pytz import timezone
import pytz

# @param request Has a desired time and we return the swipes available
#                at each dining hall
# TODO: implement location filtering too
# returns a JSON of dining hall names with lowest ask and highest bid


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def get_swipes(request):
    """
    Return swipe data for each dining hall; used to populate main page

    Args:
        request (Request): does't use arg

    Returns:
        JSON: dining halls with the lowest swipe available and total number of swipes {"Hall": {"nBids": 1, "nSwipes": 1, "times": {"start": 17, "end": 20}}}
    """

    hallsList = ["FEAST at Rieber", "De Neve", "Covel", "Bruin Plate"]
    quickList = ["Bruin Cafe", "Cafe 1919", "Rendezvous", "The Study at Hedrick"]

    hallData = {"halls":[], "quick":[]}
    halls = DiningHall.objects.all()

    date = datetime.datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    curTime = date.time().hour

    for hall in halls:

        curId = hall.hall_id
        curName = hall.name

        # see if hall is currently open
        hours = hall.hours
        times = {'start': 0, 'end': 0}
        for h in hours:
            start = h['start'].hour
            end   = h['end'].hour
            if start <= curTime and curTime <= end:
                times['start'] = start
                times['end']   = end

        # get stats for number of swipes and bids
        swipes = Swipe.objects.filter(location=curId)
        nSwipes  = swipes.count()

        bids = Bid.objects.filter(location=curId)
        nBids = bids.count()

        # insert curHall into hallData
        curHall = {hall.name: {"nBids": nBids, "nSwipes": nSwipes, "times": times}}
        if curName in hallsList:
            hallData["halls"].append(curHall)
        elif curName in quickList:
            hallData["quick"].append(curHall)

    return Response(json.dumps(hallData), status=status.HTTP_200_OK)

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
