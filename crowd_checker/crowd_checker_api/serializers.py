from rest_framework import serializers

from .models import Establishments, EstablishmentStatus, GeoLocation, Location, GteSmallWithReviewDate, \
    GteSmallWithoutReviewDate


class GteSmallWithReviewDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GteSmallWithReviewDate
        fields = '__all__'

class GteSmallWithoutReviewDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GteSmallWithoutReviewDate
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class GeoLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoLocation
        fields = '__all__'


class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishments
        fields = '__all__'


class EstablishmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstablishmentStatus
        exclude = ['datetime']

