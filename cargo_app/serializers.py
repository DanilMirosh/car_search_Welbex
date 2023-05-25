from rest_framework import serializers
from .models import Location, Cargo, Car


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CargoSerializer(serializers.ModelSerializer):
    nearby_cars_count = serializers.SerializerMethodField()
    car_distances = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = '__all__'

    def get_nearby_cars_count(self, obj):
        return obj.nearby_cars_count()

    def get_car_distances(self, obj):
        return obj.car_distances()


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
