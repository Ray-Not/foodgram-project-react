# myapp/management/commands/load_data_from_json.py
import json

from django.core.management.base import BaseCommand
from food.models import Ingredient


class Command(BaseCommand):
    help = 'Load data from JSON file into database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']

        with open(json_file, 'r', encoding='UTF-8') as file:
            data = json.load(file)

            for item in data['ingredients']:
                ingredient = Ingredient(
                    name=item['name'],
                    measurement_unit=item['measurement_unit'],
                )
                ingredient.save()
