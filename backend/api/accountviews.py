from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from api.models import Account, User, Location, Bid, Swipe
from api.serializers import LocationSerializer, AccountSerializer
from django.core import serializers
import json
import datetime

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def account_checkexistence(request):
    """
    Checks whether an account with the specified email exists in the database or not.

    Args:
        request (Request): Contains the email of the desired Account in the database.

    Returns:
        Reponse: HTTP_200_OK along with the user_id if it exists or HTTP_400_BAD_REQEST if the request data does not
        contain an email field.
    """

    data = request.data
    if 'email' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED EMAIL ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        acc_obj = Account.objects.get(email=data['email'])
        return Response({'exists': '1', 'user_id': acc_obj.user_id, 'STATUS': '0'}, status=status.HTTP_200_OK)
    except Account.DoesNotExist:
        return Response({'exists': '0', 'STATUS': '0'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def account_shouldupdatelocation(request):
	data = request.data
	if 'user_id' not in data:
		return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
	try:
		acc_obj = Account.objects.get(user_id=data['user_id'])
		should_delete = '1' if acc_obj.cur_loc is not None else '0' # Assume at first that we should delete their location if it exists unless proven otherwise
		should_update = '0' # Assume at first we shouldn't update their location unless we get proven otherwise
		active_objs = list(Bid.objects.filter(status=0, buyer_id=data['user_id'])) + list(Swipe.objects.filter(status=0, seller_id=data['user_id']))
		if len(active_objs) > 0:
			now = datetime.datetime.now()
			hour_from_now = now + datetime.timedelta(minutes=60)
			for active_obj in active_objs:
				for interval in active_obj.visibility:
					if (now.time() >= interval['start'].time() and now.time() <= interval['end'].time()) or hour_from_now.time() >= interval['start'].time():
						should_update = '1'
						should_delete = None
				if should_update == '1':
					break
		if should_delete == '1':
			cur_loc = acc_obj.cur_loc
			cur_loc.delete()
			acc_obj.cur_loc = None
			acc_obj.save()
		return Response({'should_update': should_update, 'deleted_location': should_delete, 'STATUS': '0', 'REASON': 'SUCCESSFULLY EVALUATED ACCOUNT'}, status=status.HTTP_200_OK)
	except Account.DoesNotExist:
		return Response({'STATUS': '1', 'REASON': 'NO ACCOUNT EXISTS WITH GIVEN USER_ID'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def account_updatelocation(request):
	data = request.data
	if 'user_id' not in data:
		return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED USER_ID ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
	if 'lat' not in data or 'lng' not in data:
		return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED LAT/LNG ARGUMENTS'}, status=status.HTTP_400_BAD_REQUEST)
	try:
		acc_obj = Account.objects.get(user_id=data['user_id'])
		loc_serializer = LocationSerializer(acc_obj.cur_loc, data=data) # No partial=True since we always need to specify a full location
		if loc_serializer.is_valid():
			loc_obj = loc_serializer.save()
			if acc_obj.cur_loc is None: # No location currently associated with account [either never existed or nothing currently there], assign the two together
				acc_serializer = AccountSerializer(acc_obj, data={'cur_loc': loc_obj.loc_id}, partial=True)
				if acc_serializer.is_valid():
					acc_serializer.save()
				else:
					return Response({'STATUS': '1', 'REASON': 'ACCOUNT SERIALIZER ERROR', 'ERRORS': {**acc_serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)
			return Response({'STATUS': '0', 'REASON': 'ACCOUNT LOCATION SUCCESSFULLY UPDATED'}, status=status.HTTP_200_OK)
		else:
			return Response({'STATUS': '1', 'REASON': 'LOCATION SERIALIZER ERROR', 'ERRORS': {**loc_serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)
	except Account.DoesNotExist:
		return Response({'STATUS': '1', 'REASON': 'NO ACCOUNT EXISTS WITH GIVEN USER_ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def account_create(request):
    """
    Creates a new Account and saves it in the database.

    Args:
            request (Request): An object containing data needed to create a new Account.

    Returns:
            Reponse: An HTTP response indicating that the new Account was successfully saved in the database or that there
            was an error and the Account object was not created.
    """
    data = request.data
    if 'loc' in data:
        loc_data = data.pop('loc')
        if type(loc_data) == dict:  # If we've got a dict, that means the Location object should be created from the lat/lng
            loc_serializer = LocationSerializer(data=loc_data)
            if loc_serializer.is_valid():
                loc_obj = loc_serializer.save()
                data['cur_loc'] = loc_obj.loc_id
            else:
                return Response({'STATUS': '1', 'REASON': 'LOCATION SERIALIZER ERROR', 'ERRORS': {**loc_serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)
        else:  # For testing purposes, don't create a Location object but just toss in an existing primary key
            data['cur_loc'] = loc_data
    acc_serializer = AccountSerializer(data=data)
    if acc_serializer.is_valid():
        acc_obj = acc_serializer.save()
        return Response({'STATUS': '0', 'REASON': 'SUCCESSFULLY CREATED ACCOUNT OBJECT', 'user_id': acc_obj.user_id}, status=status.HTTP_200_OK)
    else:
        return Response({'STATUS': '1', 'REASON': 'ACCOUNT SERIALIZER ERROR', 'ERRORS': {**acc_serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def account_update(request):
    """
    Updates the information in an existing Account within the database.

    Args:
        request (Request): An object containing the new data to be placed into the Account object.

    Returns:
        Response: An HTTP response that indicates whether the Account was successfully updated or if there was an error.
    """

    data = request.data
    if 'email' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED EMAIL ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        acc_obj = Account.objects.get(email=data['email'])
    except Account.DoesNotExist:
        return Response({'STATUS': '1', 'REASON': 'NO ACCOUNT EXISTS WITH GIVEN USER_ID'}, status=status.HTTP_400_BAD_REQUEST)
    if 'loc' in data:
        loc_data = data.pop('loc')
        loc_serializer = LocationSerializer(acc_obj.cur_loc, data=loc_data)
        if loc_serializer.is_valid():
            loc_obj = loc_serializer.save()
            if acc_obj.cur_loc is None: # Since location is optional on registration, we might need to assign a location ID if it's null in the existing object
            	data['cur_loc'] = loc_obj.loc_id
        else:
            return Response({'STATUS': '1', 'REASON': 'LOCATION SERIALIZER ERROR', 'ERRORS': {**loc_serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)
    acc_serializer = AccountSerializer(acc_obj, data=data, partial=True)
    if acc_serializer.is_valid():
        acc_serializer.save()
        return Response({'STATUS': '0', 'REASON': 'SUCCESSFULLY UPDATED ACCOUNT'}, status=status.HTTP_200_OK)
    return Response({'STATUS': '1', 'REASON': 'ACCOUNT SERIALIZER ERROR', 'ERRORS': {**acc_serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def account_data(request):
    """
    Returns the bids and swipes that a user is associated with to display in the frontend

    Args:
        request (Request): contains user_id

    Returns:
        a JSON whose format is r = {"Bids": {"Pending": [], "Accepted": [] }, "Swipes": {"Available": [], "Sold": [] }}
    """

    data = request.data
    if 'user_id' not in data:
        return Response({'STATUS': '1', 'REASON': 'MISSING REQUIRED user_id ARGUMENT'}, status=status.HTTP_400_BAD_REQUEST)

    user_id = data['user_id']
    r = {
        "Bids": {
            "Pending": [],
            "Accepted": []
        },
        "Swipes": {
            "Available": [],
            "Sold": []
        }
    }

    # Bids
    bids_pending = Bid.objects.filter(buyer=user_id, status=0)
    r["Bids"]["Pending"] = bid_filter(bids_pending)

    bids_accepted = Bid.objects.filter(buyer=user_id, status=1)
    r["Bids"]["Accepted"] = bid_filder(bids_accepted)

    # Swipes
    swipes_available = Swipe.objects.filter(seller=user_id, status=0)
    r["Swipes"]["Available"] = bid_filter(swipes_available)

    swipes_sold = Swipe.objects.filter(seller=user_id, status=1)
    r["Swipes"]["Sold"] = bid_filter(swipes_sold)

    return Response(r, status=status.HTTP_200_OK)


def bid_filter(bids):
    """
    Given a list of Bid objects, return a list with the serialized JSON Objects

    Args:
        bids - A list of Bid objects

    Returns:
        serialized_bids - list of Bid objects in JSON form
    """

    serialized_bids = []

    for bid in bids:
        serial = serializers.serialize("json", [bid])
        serial = json.loads(serial)
        serialized_bids.append(serial[0]["fields"])

    return serialized_bids