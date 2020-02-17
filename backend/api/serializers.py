from rest_framework import serializers
import api.models as api


class LocationSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    lat = serializers.DecimalField()
    lng = serializers.DecimalField()

    def create(self, validated_data):
        return api.Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.lng = validated_data.get('lng', instance.lng)
        instance.save()
        return instance


class DiningHallSerializer(serializers.Serializer):
    open_at = serializers.TimeField()
    close_at = serializers.TimeField()
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=200)
    picture = serializers.URLField()

    def create(self, validated_data):
        return api.DiningHall.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.open_at = validated_data.get('open_at', instance.open_at)
        instance.close_at = validated_data.get('close_at', instance.close_at)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()
        return instance


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    status = serializers.CharField(max_length=1)
    pp_email = serializers.EmailField()

    def create(self, validated_data):
        return api.User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = serializers.get('id', instance.id)
        instance.status = serializers.get('status', instance.status)
        instance.pp_email = serializers.EmailField('pp_email', instance.pp_email)
        instance.save()
        return instance
