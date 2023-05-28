from django.db.models import Count, Subquery, OuterRef
from django.db.models import Q
from django.shortcuts import get_object_or_404
from geopy.distance import distance as geopy_distance
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Location, Car, Cargo
from .serializers import (
    LocationSerializer,
    CarSerializer,
    CargoSerializer,
    CargoCreateSerializer,
    CargoUpdateSerializer,
)


class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class CarListCreateView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CargoListCreateView(generics.ListCreateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    def create(self, request, *args, **kwargs):
        serializer = CargoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CargoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CargoUpdateSerializer
        return self.serializer_class

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if 'pickup_zip' in request.data:
            pickup_zip = request.data.pop('pickup_zip')
            pickup_location = get_object_or_404(Location, zip=pickup_zip)
            request.data['pickup_location'] = pickup_location.id

        if 'delivery_zip' in request.data:
            delivery_zip = request.data.pop('delivery_zip')
            delivery_location = get_object_or_404(Location, zip=delivery_zip)
            request.data['delivery_location'] = delivery_location.id

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CargoFilterListView(generics.ListAPIView):
    serializer_class = CargoSerializer

    def get_queryset(self):
        miles = 450

        subquery = Car.objects.filter(
            Q(current_location=OuterRef('pickup_location')) | Q(current_location=OuterRef('delivery_location'))
        ).annotate(
            distance=geopy_distance(
                'current_location__latitude',
                'current_location__longitude',
                'pickup_location__latitude',
                'pickup_location__longitude',
            ),
        ).values('cargo').filter(distance__lte=miles)

        queryset = Cargo.objects.annotate(
            nearest_cars=Count(Subquery(subquery))
        )

        return queryset


class CarLocationUpdateView(generics.UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        new_location = Location.objects.exclude(id=instance.current_location.id).order_by('?').first()
        instance.current_location = new_location
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
