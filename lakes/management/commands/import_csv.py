import csv
from django.core.management.base import BaseCommand
from lakes.models import Lake
import os

class Command(BaseCommand):
    help = 'Import data from CSV'

    def handle(self, *args, **kwargs):
        """
        Import lake data from a CSV file into the database.

        - Deletes existing lake records
        - Loads data from Lakes_data.csv
        - Creates new Lake objects in bulk
        """
        # Remove existing data to avoid duplicates
        Lake.objects.all().delete()
        file_path = os.path.join(os.path.dirname(__file__), 'Lakes_data.csv')
        with open(file_path, newline='', encoding='utf-8') as file:
            # Hardcoded delimiter to match data file
            reader = csv.reader(file, delimiter=';')
            objects = []
            for row in reader:
                # Skip rows that do not contain required number of fields
                if len(row) < 2:
                    continue
                objects.append(Lake(
                    name=row[0],
                    country=row[1],
                ))
            
            # Insert all objects in a single query for better performance
            Lake.objects.bulk_create(objects)

        self.stdout.write(self.style.SUCCESS('CSV data imported'))