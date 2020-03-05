from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import DiningHall, Swipe, Bid
from api.serializers import BidSerializer, SwipeSerializer
import datetime


def bid_getcheapestswipe(hall_id, swipe_time=None, swipe_price=None):
    """
    Gets the cheapest Swipe object that meets the criteria for a specific Bid.

    Args:
            hall_id (string): The DiningHall identifier.
            swipe_time (DateTime, optional): The time range specified on the Bid. Defaults to None.
            swipe_price (Float, optional): The desired swipe price. Defaults to None.

    Returns:
            Swipe: A swipe that meets the criteria specified in the Bid, or None if no Swipes meet the criteria.
    """
    if swipe_time is None:
        swipe_time = datetime.datetime.now().time()
    else:
        swipe_time = datetime.datetime.strptime(swipe_time, "%H:%M").time()
    try:
        paired_swipe = None
        swipe_candidates = Swipe.objects.filter(status=0, location=hall_id).order_by('price', 'swipe_id')
        for swipe in swipe_candidates:
            # If a swipe price has been specified and the lowest price swipe is more expensive than desired, there aren't any eligible swipes available at this dining hall
            if swipe_price is not None and swipe_price < swipe.price:
                return None
            for hours in swipe.visibility:
                # Assuming the desired swipe time falls within the listing's range, it's a match
                if hours['start'].time() <= swipe_time and hours['end'].time() >= swipe_time:
                    paired_swipe = swipe
            if paired_swipe is not None:
                break
        return paired_swipe
    except Swipe.DoesNotExist:
        return None


@api_view(['POST'])
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
    swipe = bid_getcheapestswipe(data['hall_id'], data.get('desired_time', None), data.get(
        'price', None))  # Get the cheapest swipe for that hall at a given time
    if swipe is None and data.get('desired_time', None) is None:
        return Response({'STATUS': '1', 'REASON': 'NO ELIGIBLE SWIPES, BUT NO DESIRED TIME GIVEN TO CREATE BID'}, status=status.HTTP_400_BAD_REQUEST)
    bid_data = {'buyer': data['user_id'], 'bid_price': data.get(
        'price', None), 'location': data['hall_id'], 'desired_time': data.get('desired_time', None)}
    if swipe is not None:  # This performs the actual pairing between buyer and seller, because a match exists
        swipe_serializer = SwipeSerializer(swipe, data={'status': '1'}, partial=True)
        if swipe_serializer.is_valid():
            swipe = swipe_serializer.save()
            bid_data['status'] = '1'
            bid_data['swipe'] = swipe.swipe_id
            bid_data['bid_price'] = swipe.price
        else:
            return Response(swipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if bid_data['bid_price'] is None:
        return Response({'STATUS': '1', 'REASON': 'NO ELIGIBLE SWIPES, BUT NO DESIRED PRICE GIVEN TO CREATE BID'}, status=status.HTTP_400_BAD_REQUEST)
    bid_serializer = BidSerializer(data=bid_data)
    if bid_serializer.is_valid():
        bid_serializer.save()
        if swipe is not None:
            return Response({'STATUS': '0', 'REASON': 'BID CREATED, PAIRED WITH SWIPE'}, status=status.HTTP_200_OK)
        return Response({'STATUS': '0', 'REASON': 'BID CREATED, NO ELIGIBLE SWIPE PAIRED'}, status=status.HTTP_200_OK)
    else:
        return Response(bid_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def lowest_ask_and_highest_bid(request):
    data = request.data
    if 'hall_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED hall_id ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    if 'start' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED start ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    if 'end' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED end ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    
    info = {}

    swipe_candidates = Swipe.objects.filter(location_id=data['hall_id'], status=0).order_by('price')
    bid_candidates = Bid.objects.filter(location_id=data['hall_id'], status=0).order_by('bid_price')

    for i in range(int(data['start']), int(data['end']) + 1):
        info[i] = {}
        for j in range(i, int(data['end']) + 1):
            info[i][j] = {}
            info[i][j]["low"] = get_lowest_swipe(swipe_candidates, i, j)
            info[i][j]["high"] = get_highest_bid(bid_candidates, i, j)

    return Response(info, status=status.HTTP_200_OK)

def get_lowest_swipe(swipe_candidates, start, end):
    curr_price = "999999"
    for swipe in swipe_candidates:
        for hours in swipe.visibility:
            print(hours['start'], hours['end'])
            curr_start = str(hours['start']).split(" ")[1].split(":")[0] 
            curr_end = str(hours['end']).split(" ")[1].split(":")[0] 
            if int(curr_start) <= start and int(curr_end) >= end:
                curr_price = min(curr_price, swipe.price)
  
    return "0" if curr_price == "999999" else curr_price

def get_highest_bid(bid_candidates, start, end):
    curr_price = "0"
    for bid in bid_candidates:
        if bid.desired_time == None:
            curr_price = max(curr_price, int(bid.bid_price))
        else:
            print (bid.desired_time)
            bid_time = str(bid.desired_time).split(" ") 
            bid_time = bid_time if len(bid_time) == 1 else bid_time[1]
            curr_desired_time = "".join(bid_time).split(":")[0]
            if start <= int(curr_desired_time) <= end:
                curr_price = max(curr_price, bid.bid_price)
    return curr_price
