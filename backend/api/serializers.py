from rest_framework import serializers
import api.models as models


class LocationSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    lat = serializers.DecimalField()
    lng = serializers.DecimalField()