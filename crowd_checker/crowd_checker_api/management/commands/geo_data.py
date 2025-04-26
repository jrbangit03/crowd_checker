import os
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from ...models import GeoLocation


def get_shp_files(parent_folder: str) -> list:
    return [os.path.abspath(os.path.join(dir, f))
            for dir, path, files in os.walk(parent_folder)
            for f in files if f.endswith(".shp")]


class Command(BaseCommand):
    help = 'Pre-populates Geo data into GeoData model'
    def handle(self, *args, **kwargs):
        with transaction.atomic():
            shp_files = get_shp_files("/Users/jrbangit03/Desktop/CSCI_205_Prog_with_DB/philippines-latest-free_shp/")
            mapping = {
                'osm_id': 'osm_id',
                'location_class': 'fclass',
                'name': 'name',
                'geometry': 'POINT'
            }

            for shp_file in shp_files:
                try:
                    lm = LayerMapping(model=GeoLocation,
                                      data=shp_file,
                                      mapping=mapping,
                                      transform=False)
                    lm.save(strict=True, verbose=True)
                except Exception as e:
                    print(f"error --> file {shp_file} --> {e}")
