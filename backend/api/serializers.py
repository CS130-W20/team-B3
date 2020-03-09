from rest_framework import serializers
import api.models as api
import datetime


class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer class for Location Obejcts.
    """
    class Meta:
        model = api.Location
        fields = ['lat', 'lng']


class TimeRangeSerializer(serializers.Serializer):
    """
    Serializer class for TimeRange Objects.
    """

    start = serializers.TimeField(format=None)
    end = serializers.TimeField(format=None)


class DiningHallSerializer(LocationSerializer):
    """
    Serializer for DiningHall objects. Inherits from LocationSerializer.
    """
    # Nested serializer used for verifying that the various hours a dining hall is open (different meal periods) are valid
    hours = TimeRangeSerializer(many=True)

    class Meta(LocationSerializer.Meta):
        model = api.DiningHall
        fields = LocationSerializer.Meta.fields + ['hall_id', 'hours', 'name', 'description', 'picture']

    def create(self, validated_data):
        """
        Creates a new DiningHall object.

        Args:
            validated_data (dict): Validated DiningHall data used to create the DiningHall object.

        Returns:
            DiningHall: Newly created dining hall object.
        """

        hour_data = validated_data.pop('hours')
        hour_objs = []
        for hour_range in hour_data:
            hour_objs.append({k: datetime.datetime.combine(datetime.date.today(), v)
                              for k, v in dict(hour_range).items()})
        validated_data['hours'] = hour_objs
        hall = api.DiningHall.objects.create(**validated_data)
        return hall

    def update(self, instance, validated_data):
        """
        Updates data in the database corresponding to a specific DiningHall object.

        Args:
            instance (DiningHall): An instance of a DiningHall.
            validated_data (dict): The updated data.

        Returns:
            DiningHall: The updated DiningHall object.
        """

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
    """
    Serializer for User objects.
    """
    class Meta:
        model = api.User
        fields = ['status', 'user_id', 'pp_email']


class AccountSerializer(UserSerializer):
    """
    Serializer for Account objects.
    """
    class Meta(UserSerializer.Meta):
        model = api.Account
        fields = UserSerializer.Meta.fields + ['home_loc', 'pw', 'phone']


class SwipeSerializer(serializers.ModelSerializer):
    """
    Serializer for Swipe objects.
    """
    visibility = TimeRangeSerializer(many=True)

    class Meta:
        model = api.Swipe
        fields = ['swipe_id', 'status', 'seller', 'location', 'price', 'visibility']

    def create(self, validated_data):
        """
        Creates a new Swipe object.

        Args:
            validated_data (dict): The data used to create a new Swipe object.

        Returns:
            Swipe: The new Swipe object.
        """

        visibility_data = validated_data.pop('visibility')
        visibility_objs = []
        for hour_range in visibility_data:
            visibility_objs.append({k: datetime.datetime.combine(datetime.date.today(), v)
                                    for k, v in dict(hour_range).items()})
        validated_data['visibility'] = visibility_objs
        swipe = api.Swipe.objects.create(**validated_data)
        return swipe

    def update(self, instance, validated_data):
        """
        Updates an existing Swipe object and the data corresponding to it in the database.

        Args:
            instance (Swipe): The outdated Swipe object.
            validated_data (dict): The new data to be placed in the outdated Swipe object.

        Returns:
            Swipe: The updated Swipe object.
        """

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
    """
    Serializer for Bid objects.
    """
    class Meta:
        model = api.Bid
        fields = ['bid_id', 'status', 'swipe', 'buyer', 'location', 'bid_price', 'desired_time']


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction objects.
    """
    class Meta:
        model = api.Transaction
        fields = ['t_id', 'sender', 'recipient', 'paid', 'total', 'details']
