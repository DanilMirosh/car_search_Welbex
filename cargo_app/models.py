from django.db import models
from geopy.distance import geodesic
from random import choice


class Location(models.Model):
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Cargo(models.Model):
    pick_up_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pick_up_cargos')
    delivery_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='delivery_cargos')
    weight = models.IntegerField()
    description = models.TextField()

    def nearby_cars_count(self):
        pick_up_distance = geodesic(
            (self.pick_up_location.latitude, self.pick_up_location.longitude),
            (self.delivery_location.latitude, self.delivery_location.longitude)
        ).miles
        return Car.objects.filter(
            current_location__isnull=False,
            current_location__distance__lte=pick_up_distance
        ).count()

    def car_distances(self):
        pick_up_distance = geodesic(
            (self.pick_up_location.latitude, self.pick_up_location.longitude),
            (self.delivery_location.latitude, self.delivery_location.longitude)
        ).miles
        car_list = Car.objects.filter(
            current_location__isnull=False,
            current_location__distance__lte=pick_up_distance
        )
        distances = {}
        for car in car_list:
            distance = geodesic(
                (car.current_location.latitude, car.current_location.longitude),
                (self.pick_up_location.latitude, self.pick_up_location.longitude)
            ).miles
            distances[car.number] = distance
        return distances


class Car(models.Model):
    number = models.CharField(max_length=5, unique=True)
    current_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='cars')
    carrying_capacity = models.IntegerField()

    def update_location(self):
        random_location = choice(Location.objects.all())
        self.current_location = random_location
        self.save()
