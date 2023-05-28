import csv
from django.core.management.base import BaseCommand
from cargo_app.models import Location


class Command(BaseCommand):
    help = 'Import locations from CSV'

    def handle(self, *args, **options):
        with open('uszips.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Location.objects.create(
                    zip_code=row['zip'],
                    latitude=float(row['lat']),
                    longitude=float(row['lng']),
                    city=row['city'],
                    state=row['state_name'],
                )
        self.stdout.write(self.style.SUCCESS('Locations imported successfully'))
