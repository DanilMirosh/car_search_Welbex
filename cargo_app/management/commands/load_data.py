import csv
from django.core.management.base import BaseCommand
from cargo_app.models import Location


class Command(BaseCommand):
    help = 'Load data from uszips.csv'

    def handle(self, *args, **options):
        with open('uszips.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    Location.objects.create(
                        city=row['city'],
                        state=row['state_id'],
                        zip_code=row['zip'],
                        latitude=float(row['lat']),
                        longitude=float(row['lng']),
                    )
                except ValueError:
                    continue
