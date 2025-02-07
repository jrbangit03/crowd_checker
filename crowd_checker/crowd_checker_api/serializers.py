from rest_framework import serializers

from .models import Establishments, EstablishmentStatus


### TO-DO: I want to use gRPC (is it possible in django?)

# This is to serialize the model into json including all fields of the model.


# Abstraction and Polymorphism

class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishments
        fields = '__all__'


class EstablishmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstablishmentStatus
        exclude = ['datetime']

