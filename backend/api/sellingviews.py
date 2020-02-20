from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import SwipeSerializer


@api_view(['POST'])
def sell_swipe(request):
    data = request.data
    data['status'] = '1'
    swipe = SwipeSerializer(data=data)
    if swipe.is_valid():
        swipe.save()
        return Response({'STATUS': '0'}, status=status.HTTP_200_OK)
    else:
        return Response(swipe.errors, status=status.HTTP_400_BAD_REQUEST)
