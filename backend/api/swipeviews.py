from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import DiningHall, Account, User, Swipe, Bid
from api.serializers import SwipeSerializer, BidSerializer

import json

# @param request Has a time range and we return the swipes available
#                at each dining hall
# TODO: implement location filtering too
# returns a JSON of dining hall names with lowest ask and highest bid

@api_view(['GET'])
def get_swipes(request):

    hallData = {}

    halls = DiningHall.objects.all()

    for hall in halls:

        currId   = hall.hall_id

        hallBids = Swipe.objects.filter(location=currId)
        lowest = hallBids.order_by('price')[0].price
        count  = hallBids.count()

        hallData[hall.name] = {"lowest": lowest, "count": count}

    return Response(json.dumps(hallData), status=status.HTTP_200_OK)
