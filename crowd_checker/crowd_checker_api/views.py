from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Establishments, EstablishmentStatus
from .serializers import EstablishmentSerializer, EstablishmentStatusSerializer


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


class EstablishmentStatusView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EstablishmentStatusView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        establishments_status = EstablishmentStatus.objects.all()
        serialized_establishments_status = EstablishmentStatusSerializer(establishments_status, many=True)
        return Response(serialized_establishments_status.data, status=status.HTTP_200_OK)


    def post(self, request):
       data = {k: v for k, v in  request.data.items() if k != 'datetime'}
       serialized_data = EstablishmentStatusSerializer(data=data)
       if serialized_data.is_valid():
           serialized_data.save()
           return Response(serialized_data.data, status=status.HTTP_201_CREATED)
