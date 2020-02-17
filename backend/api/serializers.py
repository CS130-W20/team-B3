from rest_framework import serializers
import api.models as api


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = api.Location
        fields = ['id', 'lat', 'lng']


class DiningHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = api.DiningHall
        fields = ['open_at', 'close_at', 'name', 'description', 'picture']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = api.User
        fields = ['status', 'id', 'pp_email']


class AccountSerializer(serializers.ModelSerializer):
    home_loc = LocationSerializer()

    class Meta:
        model = api.Account
        fields = ['home_loc', 'pw', 'phone']


class SwipeSerializer(serializers.ModelSerializer):
    seller = UserSerializer()

    class Meta:
        model = api.Swipe
        fields = ['status', 'seller', 'location', 'price']


class BidSerializer(serializers.ModelSerializer):
    swipe = SwipeSerializer()
    buyer = UserSerializer()

    class Meta:
        model = api.Bid
        fields = ['status', 'swipe', 'buyer', 'bid_price']
