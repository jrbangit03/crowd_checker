from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Establishments
from .serializers import EstablishmentSerializer


def get_establishments(request):

    establishments = Establishments.objects.all()
    serialized_establishments = EstablishmentSerializer(establishments, many=True)
    return Response(serialized_establishments.data, status=status.HTTP_200_OK)


def add_establishment(request):
    serialized_data = EstablishmentSerializer(data=request.data)
    if serialized_data.is_valid():
        serialized_data.save()
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def establishments(request):
    if request.method == 'GET':
        return get_establishments(request)
    elif request.method == 'POST':
        return add_establishment(request)