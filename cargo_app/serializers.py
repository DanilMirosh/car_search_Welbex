from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_gis.serializers import GeometryField

from .models import Location, Car, Cargo, CargoCar


class LocationSerializer(serializers.ModelSerializer):
    point = GeometryField()

    class Meta:
        model = Location
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    current_location = LocationSerializer()

    class Meta:
        model = Car
        fields = '__all__'


class CargoCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoCar
        fields = '__all__'


class CargoSerializer(serializers.ModelSerializer):
    pickup_zip = serializers.CharField(source='pick_up_location.zip_code', read_only=True)
    delivery_zip = serializers.CharField(source='delivery_location.zip_code', read_only=True)
    nearest_cars = serializers.IntegerField(source='nearest_cars', read_only=True)

    class Meta:
        model = Cargo
        fields = ['id', 'pickup_zip', 'delivery_zip', 'weight', 'description', 'nearest_cars']


class CargoCreateSerializer(serializers.ModelSerializer):
    pickup_zip = serializers.CharField(write_only=True)
    delivery_zip = serializers.CharField(write_only=True)

    class Meta:
        model = Cargo
        fields = ['pickup_zip', 'delivery_zip', 'weight', 'description']

    def create(self, validated_data):
        pickup_zip = validated_data.pop('pickup_zip')
        delivery_zip = validated_data.pop('delivery_zip')

        pickup_location = get_object_or_404(Location, zip_code=pickup_zip)
        delivery_location = get_object_or_404(Location, zip_code=delivery_zip)

        validated_data['pick_up_location'] = pickup_location
        validated_data['delivery_location'] = delivery_location

        cargo = super().create(validated_data)

        return cargo


class CargoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['weight', 'description']
