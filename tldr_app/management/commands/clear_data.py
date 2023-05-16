from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Clears all table data from the database'

    def handle(self, *args, **options):
        for model in apps.get_models():
            model.objects.all().delete()