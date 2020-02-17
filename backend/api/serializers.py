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
        instance.open_at = serializers.TimeField()
        instance.close_at = serializers.TimeField()
        instance.name = serializers.CharField(max_length=50)
        instance.description = serializers.CharField(max_length=200)
        instance.picture = serializers.URLField()
        instance.save()
        return instance
