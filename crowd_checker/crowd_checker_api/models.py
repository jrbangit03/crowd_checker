from django.db import models


class Establishments(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
