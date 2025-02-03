from django.db import models


# Encapsulating all model related operations here.

# A class that inherits the Model.
# Each instance of this class will contain data that represents a row,
# this allows us to manipulate the data in object-oriented manner.
class Establishments(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
