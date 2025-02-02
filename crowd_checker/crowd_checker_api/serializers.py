from rest_framework import serializers

from .models import Establishments


### TO-DO: I want to use gRPC

# This is to serialize the model into json including all fields of the model.
class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishments
        fields = '__all__'
