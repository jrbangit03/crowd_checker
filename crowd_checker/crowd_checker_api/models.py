from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.gis.db import models as geomodels
from pgvector.django import VectorField



##############Term Paper Reqs#################

class GteSmallBaseline(geomodels.Model):
    review_id = models.CharField(primary_key=True)
    fsq_id = models.CharField()
    name = models.CharField()
    branch = models.CharField()
    feedback = models.CharField(null=True)
    location = geomodels.PointField()
    embeddings = VectorField(
        dimensions=384,
        help_text="Vector embeddings for reviews of places and supporting metadata",
        null=True,
        blank=True,
    )

class GteSmallWithReviewDate(geomodels.Model):
    review_id = models.CharField(primary_key=True)
    fsq_id = models.CharField()
    name = models.CharField()
    branch = models.CharField()
    feedback = models.CharField(null=True)
    location = geomodels.PointField()
    embeddings = VectorField(
        dimensions=384,
        help_text="Vector embeddings for reviews of places and supporting metadata",
        null=True,
        blank=True,
    )

class GteSmallWithoutReviewDate(geomodels.Model):
    review_id = models.CharField(primary_key=True)
    fsq_id = models.CharField()
    name = models.CharField()
    branch = models.CharField()
    feedback = models.CharField(null=True)
    location = geomodels.PointField()
    embeddings = VectorField(
        dimensions=384,
        help_text="Vector embeddings for reviews of places and supporting metadata",
        null=True,
        blank=True,
    )

class OpenAISmallWithReviewDate(geomodels.Model):
    review_id = models.CharField(primary_key=True)
    fsq_id = models.CharField()
    name = models.CharField()
    branch = models.CharField()
    feedback = models.CharField(null=True)
    location = geomodels.PointField()
    embeddings = VectorField(
        dimensions=1536,
        help_text="Vector embeddings for reviews of places and supporting metadata",
        null=True,
        blank=True,
    )

class OpenAISmallWithoutReviewDate(geomodels.Model):
    review_id = models.CharField(primary_key=True)
    fsq_id = models.CharField()
    name = models.CharField()
    branch = models.CharField()
    feedback = models.CharField(null=True)
    location = geomodels.PointField()
    embeddings = VectorField(
        dimensions=1536,
        help_text="Vector embeddings for reviews of places and supporting metadata",
        null=True,
        blank=True,
    )

##############Term Paper Reqs#################

class Location(geomodels.Model):
    fsq_id = models.CharField(primary_key=True)
    name = models.CharField()
    country = models.CharField(null=True)
    locality = models.CharField(null=True)
    location_type = ArrayField(models.CharField())
    geometry = geomodels.PointField()

class Review(geomodels.Model):
    review_id = models.CharField(primary_key=True)
    fsq_id = models.CharField()
    name = models.CharField()
    branch = models.CharField()
    feedback = models.CharField(null=True)
    embeddings = VectorField(
        dimensions=384,
        help_text="Vector embeddings for reviews of places",
        null=True,
        blank=True,
    )


class GeoLocation(geomodels.Model):
    osm_id = geomodels.CharField(null=True)
    location_class = geomodels.CharField(null=True)
    name = geomodels.CharField(null=True)
    geometry = geomodels.PointField()


class EstablishmentStatus(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now=True)



class Establishments(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def save(self, *args, **kwargs):
        # do some validation before saving
        super(Establishments, self).save()


    def delete(self, *args, **kwargs):
        # do some validation before deleting
        super(Establishments, self).delete()

