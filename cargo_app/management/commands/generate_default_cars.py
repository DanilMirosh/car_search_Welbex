import random
from django.core.management.base import BaseCommand
from cargo_app.models import Car


class Command(BaseCommand):
    help = 'Generate default cars'

    def handle(self, *args, **options):
        cars = [
            Car(
                unique_number=f"{random.randint(1000, 9999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}",
                latitude=random.uniform(-90, 90),
                longitude=random.uniform(-180, 180),
                capacity=random.randint(500, 1000)
            )
            for _ in range(20)
        ]
        Car.objects.bulk_create(cars)
        self.stdout.write(self.style.SUCCESS('Default cars generated successfully'))
