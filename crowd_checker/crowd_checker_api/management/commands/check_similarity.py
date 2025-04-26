
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Pre-populates Geo data into GeoData model'
    def handle(self, *args, **kwargs):
        pass