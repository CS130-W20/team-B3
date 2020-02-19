from rest_framework import serializers
import api.models as api
import datetime

class LocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = api.Location
		fields = ['lat', 'lng']

class TimeRangeSerializer(serializers.Serializer):
	start = serializers.TimeField()
	end = serializers.TimeField()


class DiningHallSerializer(LocationSerializer):
	hours = TimeRangeSerializer(many=True) # Nested serializer used for verifying that the various hours a dining hall is open (different meal periods) are valid
	class Meta(LocationSerializer.Meta):
		model = api.DiningHall
		fields = LocationSerializer.Meta.fields + ['hours', 'name', 'description', 'picture']

	def create(self, validated_data):
		hour_data = validated_data.pop('hours')
		hour_objs = []
		for hour_range in hour_data:
			hour_objs.append({k: datetime.datetime.combine(datetime.date.today(), v) for k, v in dict(hour_range).items()})
		validated_data['hours'] = hour_objs
		hall = api.DiningHall.objects.create(**validated_data)
		return hall


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
		fields = ['listing', 'status', 'seller', 'location', 'price']


class BidSerializer(serializers.ModelSerializer):
	class Meta:
		model = api.Bid
		fields = ['status', 'swipe', 'buyer', 'bid_price']


class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = api.Transaction
		fields = ['sender', 'recipient', 'paid', 'total', 'details']


class ListingSerializer(serializers.ModelSerializer):
	visibility = TimeRangeSerializer(many=True) # Since we have a nested serializer, we need to override the create method :|
	class Meta:
		model = api.Listing
		fields = ['seller_loc', 'description', 'visibility']

	def create(self, validated_data):
		visibility_data = validated_data.pop('visibility')
		visibility_objs = []
		for hour_range in visibility_data:
			visibility_objs.append({k: datetime.datetime.combine(datetime.date.today(), v) for k, v in dict(hour_range).items()})
		validated_data['visibility'] = visibility_objs
		listing = api.Listing.objects.create(**validated_data)
		return listing
	
