import random
from django.core.management.base import BaseCommand
from cargo_app.models import Car, Location


class Command(BaseCommand):
    help = 'Generate default cars'

    def handle(self, *args, **options):
        locations = list(Location.objects.all())
        cars = [
            Car(
                unique_number=f"{random.randint(1000, 9999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}",
                current_location=random.choice(locations),
                capacity=random.randint(500, 1000)
            )
            for _ in range(20)
        ]
        Car.objects.bulk_create(cars)
        self.stdout.write(self.style.SUCCESS('Default cars generated successfully'))
