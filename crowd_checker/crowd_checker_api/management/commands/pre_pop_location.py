import uuid

from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping


from ...models import GeoLocation, Review, GteSmallWithReviewDate, GteSmallWithoutReviewDate, \
    OpenAISmallWithoutReviewDate, OpenAISmallWithReviewDate
from ...utilities.embeddings import HuggingFaceModelEmbeddings, OpenAIModelEmbeddings
from ...utilities.foursquare_api import FourSquare


class Command(BaseCommand):
    help = 'Pre-populates Geo data into GeoData model'
    def handle(self, *args, **kwargs):
        fsq_client = FourSquare("fsq3En/s4qGjXXgK2B6/PqDQ+K8SPdfvqYC7IU3g45Uv5iM=")
        latitude = 120.9822269
        longitude = 14.5901829

        huggingface_embedder = HuggingFaceModelEmbeddings()
        openAI_embedder = OpenAIModelEmbeddings()


        extract_fsq_ids = fsq_client.extract_fsq_ids(longitude, latitude, 2000, "hotel")
        reviews = fsq_client.get_reviews(extract_fsq_ids, huggingface_embedder, include_rev_date=True)


        for review in reviews:
            # updated_rows = GteSmallWithReviewDate.objects.filter(review_id=rev.review_id,
            #                                                      fsq_id=rev.fsq_id).update(name=rev.name,
            #                                                                                branch=rev.branch,
            #                                                                                feedback=rev.feedback,
            #                                                                                location=rev.location,
            #                                                                                embeddings=rev.embeddings)
            print(review.embeddings)
            updated_rows = GteSmallWithReviewDate.objects.filter(review_id=review.review_id,
                                                                       fsq_id=review.fsq_id).update(name=review.name,
                                                                                              branch=review.branch,
                                                                                              feedback=review.feedback,
                                                                                              location=review.location,
                                                                                              embeddings=review.embeddings)
            if not updated_rows:
                GteSmallWithReviewDate(
                    review_id=review.review_id,
                    fsq_id=review.fsq_id,
                    name=review.name,
                    branch=review.branch,
                    feedback=review.feedback,
                    location=review.location,
                    embeddings=review.embeddings
                ).save()


            

