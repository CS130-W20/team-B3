from rest_framework import serializers
import api.models as api
from bson import ObjectId
from bson.errors import InvalidId


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
	home_loc = LocationSerializer()

	class Meta(UserSerializer.Meta):
		model = api.Account
		fields = UserSerializer.Meta.fields + ['home_loc', 'pw', 'phone']


	def create(self, validated_data): #When we have nested serializers like this, we have to override create behavior :|
		loc_data = validated_data.pop('home_loc')
		if type(loc_data) == dict:
			loc_obj = api.Location.objects.create(**loc_data)
		elif type(loc_data) == api.models.Location:
			loc_obj = loc_data
		account = api.Account.objects.create(home_loc=loc_obj, **validated_data)
		return account

	def update(self, instance, validated_data): #As well as update behavior
		loc_data = validated_data.pop('home_loc')
		assert type(loc_data) == dict
		loc_obj = instance.home_loc
		loc_obj.lat = loc_data.get('lat', loc_obj.lat)
		loc_obj.lng = loc_data.get('lng', loc_obj.lng)
		loc_obj.save()
		instance.status = validated_data.get('status', instance.status)
		instance.pp_email = validated_data.get('pp_email', instance.pp_email)
		instance.pw = validated_data.get('pw', instance.pw)
		return instance

class SwipeSerializer(serializers.ModelSerializer):
	seller = UserSerializer()
	location = DiningHallSerializer()

	class Meta:
		model = api.Swipe
		fields = ['status', 'seller', 'location', 'price']

	def create(self, validated_data): #To create a swipe, we need to ensure that the seller and dining hall are both valid
		loc_data = validated_data.pop('hall')
		if type(loc_data) == str:
			loc_obj = api.DiningHall.objects.get(hall_id=loc_data)
		elif type(loc_data) == api.models.DiningHall:
			loc_obj = loc_data
		seller_data = validated_data.pop('seller')
		if type(seller_data) == str:
			seller_obj = api.User.objects.get(user_id=seller_data)
		elif type(seller_data) == api.models.User:
			seller_obj = seller_data
		swipe = api.Swipe.objects.create(location=loc_obj, seller=seller_obj, **validated_data)
		return swipe



class BidSerializer(serializers.ModelSerializer):
	swipe = SwipeSerializer()
	buyer = UserSerializer()

	class Meta:
		model = api.Bid
		fields = ['status', 'swipe', 'buyer', 'bid_price']

	def create(self, validated_data): #To create a bid, we need to ensure that the swipe and buyer are both valid
		swipe_data = validated_data.pop('swipe')
		if type(swipe_data) == str:
			swipe_obj = api.Swipe.objects.get(swipe_id=swipe_data)
		elif type(swipe_data) == api.models.Swipe:
			swipe_obj = swipe_data
		buyer_data = validated_data.pop('buyer')
		if type(buyer_data) == str:
			buyer_obj = api.User.objects.get(user_id=buyer_data)
		elif type(buyer_data) == api.models.User:
			buyer_obj = buyer_data
		bid = api.Bid.objects.create(swipe=swipe_obj, buyer=buyer_obj, **validated_data)
		return bid


class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = api.Transaction
		fields = ['sender', 'recipient', 'paid', 'total', 'details']


class ListingSerializer(serializers.ModelSerializer):
	swipe = SwipeSerializer()
	seller_loc = LocationSerializer()

	class Meta:
		model = api.Listing
		fields = ['swipe', 'seller_loc', 'description', 'visible_from', 'visible_to']

	def create(self, validated_data): #We need to ensure that the swipe and the seller's location (if included) is valid
		swipe_data = validated_data.pop('swipe')
		if type(swipe_data) == str:
			swipe_obj = api.Swipe.objects.get(swipe_id=swipe_data)
		elif type(swipe_data) == api.models.Swipe:
			swipe_obj = swipe_data
		seller_loc_data = validated_data.pop('seller_loc')
		if type(seller_loc_data) == str:
			seller_loc_obj = api.Listing.objects.get(listing_id=seller_loc_data)
		elif type(seller_loc_data) == api.models.Location:
			seller_loc_obj = seller_loc_data
		listing = api.Listing.objects.create(swipe=swipe_obj, seller_loc=seller_loc_obj, **validated_data)
		return listing
