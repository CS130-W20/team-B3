from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def default(request):
    """
        Simple endpoint to check that the server is running
    """
    return Response("Welcome to the SwipeX API", status=status.HTTP_200_OK)
