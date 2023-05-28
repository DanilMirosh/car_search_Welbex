from geopy.distance import geodesic
from rest_framework import serializers
from .models import Location, Car, Cargo, CargoCar


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['city', 'state', 'zip_code', 'latitude', 'longitude']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'unique_number', 'capacity', 'latitude', 'longitude')


class CargoSerializer(serializers.ModelSerializer):
    pick_up_location = LocationSerializer()
    delivery_location = LocationSerializer()
    cars = CarSerializer(many=True, read_only=True)
    cars_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cargo
        fields = ('id', 'pick_up_location', 'delivery_location', 'weight', 'description', 'cars_count', 'cars')

    def create(self, validated_data):
        pick_up_location_data = validated_data.pop('pick_up_location')
        delivery_location_data = validated_data.pop('delivery_location')

        pick_up_location = Location.objects.get(zip_code=pick_up_location_data['zip_code'])
        delivery_location = Location.objects.get(zip_code=delivery_location_data['zip_code'])

        cars_within_distance = []
        pick_up_coordinates = (pick_up_location.latitude, pick_up_location.longitude)

        for car in Car.objects.all():
            car_coordinates = (car.latitude, car.longitude)
            distance = geodesic(pick_up_coordinates, car_coordinates).miles

            if distance <= 450:
                cars_within_distance.append(car)

        cargo = Cargo.objects.create(pick_up_location=pick_up_location,
                                     delivery_location=delivery_location,
                                     weight=validated_data['weight'],
                                     description=validated_data['description'])

        cargo.cars.set(cars_within_distance)

        return cargo

    def update(self, instance, validated_data):
        pick_up_location_data = validated_data.pop('pick_up_location', None)
        delivery_location_data = validated_data.pop('delivery_location', None)

        if pick_up_location_data:
            pick_up_location = Location.objects.get(zip_code=pick_up_location_data['zip_code'])
            instance.pick_up_location = pick_up_location

        if delivery_location_data:
            delivery_location = Location.objects.get(zip_code=delivery_location_data['zip_code'])
            instance.delivery_location = delivery_location

        instance.weight = validated_data.get('weight', instance.weight)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance


class CargoCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoCar
        fields = '__all__'
