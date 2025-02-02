from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EstablishmentSerializer


@api_view(['GET'])
def get_establishments(request):
    return Response(EstablishmentSerializer({"country":"Philippines",
                                            "city":"Manila",
                                            "name":"Robinsons Magnolia",
                                            "latitude":1231.12,
                                            "longitude":123123.31}).data)
