from rest_framework import serializers
import api.models as models


class LocationSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    lat = serializers.DecimalField()
    lng = serializers.DecimalField()

    def create(self, validated_data):
        return models.Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.lng = validated_data.get('lng', instance.lng)


