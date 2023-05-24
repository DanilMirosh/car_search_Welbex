from rest_framework import generics
from .models import Cargo, Car
from .serializers import CargoSerializer, CarSerializer


class CargoListCreateView(generics.ListCreateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class CarListCreateView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
