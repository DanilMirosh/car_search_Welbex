from django.contrib.gis.db import models


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.city


class Car(models.Model):
    unique_number = models.CharField(max_length=10)
    capacity = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f'Car {self.unique_number}'


class Cargo(models.Model):
    weight = models.IntegerField()
    description = models.CharField(max_length=255)
    pick_up_location = models.ForeignKey('Location', related_name='pick_up_cargos', on_delete=models.CASCADE)
    delivery_location = models.ForeignKey('Location', related_name='delivery_cargos', on_delete=models.CASCADE)
    cars = models.ManyToManyField('Car', related_name='cargos')

    def __str__(self):
        return f'Cargo {self.description}'


class CargoCar(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    distance = models.FloatField()
