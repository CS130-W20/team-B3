from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Account, User, Location
from api.serializers import LocationSerializer, AccountSerializer, UserSerializer

@api_view(['POST'])
def account_create(request):
	serializer = AccountSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)