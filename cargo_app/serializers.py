from rest_framework import serializers

from .models import Location, Car, Cargo, CargoCar


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['city', 'state', 'zip_code', 'latitude', 'longitude']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class CargoSerializer(serializers.ModelSerializer):
    pick_up_location = LocationSerializer()
    delivery_location = LocationSerializer()
    cars_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cargo
        fields = ('id', 'pick_up_location', 'delivery_location', 'weight', 'description', 'cars_count')


class CargoCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoCar
        fields = '__all__'
