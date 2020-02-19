from rest_framework import serializers
import api.models as api


class LocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = api.Location
		fields = ['lat', 'lng']


class DiningHallSerializer(LocationSerializer):
	class Meta(LocationSerializer.Meta):
		model = api.DiningHall
		fields = LocationSerializer.Meta.fields + ['open_at', 'close_at', 'name', 'description', 'picture']


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = api.User
		fields = ['status', 'user_id', 'pp_email']


class AccountSerializer(UserSerializer):
	class Meta(UserSerializer.Meta):
		model = api.Account
		fields = UserSerializer.Meta.fields + ['home_loc', 'pw', 'phone']


class SwipeSerializer(serializers.ModelSerializer):
	class Meta:
		model = api.Swipe
		fields = ['status', 'seller', 'location', 'price']


class BidSerializer(serializers.ModelSerializer):
	class Meta:
		model = api.Bid
		fields = ['status', 'swipe', 'buyer', 'bid_price']


class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = api.Transaction
		fields = ['sender', 'recipient', 'paid', 'total', 'details']


class ListingSerializer(serializers.ModelSerializer):
	class Meta:
		model = api.Listing
		fields = ['swipe', 'seller_loc', 'description', 'visible_from', 'visible_to']