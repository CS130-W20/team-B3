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

	def update(self, instance, validated_data):
		instance.name = validated_data.get('name', instance.name)
		instance.picture = validated_data.get('picture', instance.picture)
		instance.description = validated_data.get('description', instance.description)
		instance.lat = validated_data.get('lat', instance.lat)
		instance.lng = validated_data.get('lng', instance.lng)
		hour_data = validated_data.get('hours', instance.hours)
		hour_objs = []
		for hour_range in hour_data:
			hour_obj = {}
			for k, v in dict(hour_range).items():
				if isinstance(v, datetime.datetime):
					hour_obj[k] = v
				else:
					hour_obj[k] = datetime.datetime.combine(datetime.date.today(), v)
			hour_objs.append(hour_obj)
		instance.hours = hour_objs
		instance.save()
		return instance


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = api.User
		fields = ['status', 'user_id', 'pp_email']


class AccountSerializer(UserSerializer):
	class Meta(UserSerializer.Meta):
		model = api.Account
		fields = UserSerializer.Meta.fields + ['home_loc', 'pw', 'phone']


class SwipeSerializer(serializers.ModelSerializer):
	visibility = TimeRangeSerializer(many=True)
	class Meta:
		model = api.Swipe
		fields = ['status', 'seller', 'location', 'price', 'visibility']
	
	def create(self, validated_data):
		visibility_data = validated_data.pop('visibility')
		visibility_objs = []
		for hour_range in visibility_data:
			visibility_objs.append({k: datetime.datetime.combine(datetime.date.today(), v) for k, v in dict(hour_range).items()})
		validated_data['visibility'] = visibility_objs
		swipe = api.Swipe.objects.create(**validated_data)
		return swipe

	def update(self, instance, validated_data):
		instance.status = validated_data.get('status', instance.status)
		instance.seller = validated_data.get('seller', instance.seller)
		instance.location = validated_data.get('location', instance.location)
		instance.price = validated_data.get('price', instance.price)
		visibility_data = validated_data.get('visibility', instance.visibility)
		visibility_objs = []
		for hour_range in visibility_data:
			hour_obj = {}
			for k, v in dict(hour_range).items():
				if isinstance(v, datetime.datetime):
					hour_obj[k] = v
				else:
					hour_obj[k] = datetime.datetime.combine(datetime.date.today(), v)
			visibility_objs.append(hour_obj)
		instance.visibility = visibility_objs
		instance.save()
		return instance

class BidSerializer(serializers.ModelSerializer):
	class Meta:
		model = api.Bid
		fields = ['status', 'swipe', 'buyer', 'location', 'bid_price', 'desired_time']


class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = api.Transaction
		fields = ['sender', 'recipient', 'paid', 'total', 'details']