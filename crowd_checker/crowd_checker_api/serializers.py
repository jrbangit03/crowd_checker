from rest_framework import serializers

from .models import Establishments

### TO-DO: I want to use gRPC (is it possible in django?)

# This is to serialize the model into json including all fields of the model.

# This file will contain all of SerDe related operations (1 serializer per model)
# which promotes separation of concern that allows
# the application to be easily maintained and understand.

# The usage of ModelSerializer allows us to create different types of serializer depending on use case.
# Which exhibits polymorphism.
class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishments
        fields = '__all__'
