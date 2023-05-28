from django.db.models import Count, Q
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

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.select_related('pick_up_location', 'delivery_location')
        queryset = queryset.annotate(
            cars_count=Count(
                'cars',
                filter=Q(cargocar__distance__lte=450),
            ),
        )
        queryset = queryset.prefetch_related('cars')  # Загрузка списка машин

        for cargo in queryset:
            cargo.cars.set(cargo.cargocar_set.filter(distance__lte=450).values_list('car', flat=True))

        return queryset

    def perform_create(self, serializer):
        pick_up_zip = self.request.data.get('pick_up_location')['zip_code']
        delivery_zip = self.request.data.get('delivery_location')['zip_code']
        pick_up_location = Location.objects.get(zip_code=pick_up_zip)
        delivery_location = Location.objects.get(zip_code=delivery_zip)
        serializer.save(pick_up_location=pick_up_location, delivery_location=delivery_location)


class CargoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Получение списка номеров ВСЕХ машин с расстоянием до выбранного груза
        cargo_cars = CargoCar.objects.filter(cargo_id=data['id'])
        cars = []
        for cargo_car in cargo_cars:
            car_data = CarSerializer(cargo_car.car).data
            car_data['distance'] = cargo_car.distance
            cars.append(car_data)
        data['cars'] = cars

        return Response(data)


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
