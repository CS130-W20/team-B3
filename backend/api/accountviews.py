from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Account, User, Location
from api.serializers import LocationSerializer, AccountSerializer, UserSerializer

@api_view(['POST'])
def account_create(request):
	data = request.data
	loc_data = data.pop('loc')
	if type(loc_data) == dict: #If we've got a dict, that means the Location object should be created from the lat/lng
		loc_serializer = LocationSerializer(data=loc_data)
		if loc_serializer.is_valid():
			loc_obj = loc_serializer.save()
			data['home_loc'] = loc_obj.loc_id
		else:
			return Response(loc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	else: #For testing purposes, don't create a Location object but just toss in an existing primary key
		data['home_loc'] = loc_data
	acc_serializer = AccountSerializer(data=data)
	if acc_serializer.is_valid():
		acc_serializer.save()
		return Response({'STATUS': '0'}, status=status.HTTP_200_OK)
	else:
		return Response(acc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)