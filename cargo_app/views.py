from geopy.distance import geodesic
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Location, Car, Cargo, CargoCar
from .serializers import LocationSerializer, CarSerializer, CargoSerializer, CargoCarSerializer


class LocationListView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class CarListView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CargoListCreateView(generics.ListCreateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    def create(self, request, *args, **kwargs):
        pick_up_location_data = request.data.get('pick_up_location')
        delivery_location_data = request.data.get('delivery_location')

        pick_up_zip = pick_up_location_data['zip_code']
        delivery_zip = delivery_location_data['zip_code']
        pick_up_location = Location.objects.get(zip_code=pick_up_zip)
        delivery_location = Location.objects.get(zip_code=delivery_zip)

        cars_within_distance = []
        pick_up_coordinates = (pick_up_location.latitude, pick_up_location.longitude)

        for car in Car.objects.all():
            car_coordinates = (car.latitude, car.longitude)
            distance = geodesic(pick_up_coordinates, car_coordinates).miles

            if distance <= 450:
                cars_within_distance.append(car)

        cargo_data = {
            'pick_up_location': {
                'city': pick_up_location.city,
                'state': pick_up_location.state,
                'zip_code': pick_up_location.zip_code,
                'latitude': pick_up_location.latitude,
                'longitude': pick_up_location.longitude
            },
            'delivery_location': {
                'city': delivery_location.city,
                'state': delivery_location.state,
                'zip_code': delivery_location.zip_code,
                'latitude': delivery_location.latitude,
                'longitude': delivery_location.longitude
            },
            'cars': cars_within_distance,
            'weight': request.data.get('weight'),
            'description': request.data.get('description')
        }

        serializer = self.get_serializer(data=cargo_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CargoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CargoCarListCreateView(generics.ListCreateAPIView):
    queryset = CargoCar.objects.all()
    serializer_class = CargoCarSerializer


class CargoCarRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CargoCar.objects.all()
    serializer_class = CargoCarSerializer


class CarLocationUpdateView(generics.UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def update(self, request, *args, **kwargs):
        car = self.get_object()
        location = Location.objects.order_by('?').first()
        car.current_location = location
        car.save()
        return Response(status=status.HTTP_200_OK)
