import json
import numpy as np
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

from .models import Establishments, EstablishmentStatus, GeoLocation, GteSmallWithReviewDate, GteSmallWithoutReviewDate
from .serializers import EstablishmentSerializer, EstablishmentStatusSerializer, GeoLocationSerializer, \
    GteSmallWithReviewDateSerializer, GteSmallWithoutReviewDateSerializer
from .utilities.embeddings import HuggingFaceModelEmbeddings
from .utilities.llm_query import LLMQuery
# from .utilities.test_query import query_template

from pgvector.django import CosineDistance

from .utilities.utils import get_embedder


# 1 - gawin muna requirements -- **DONE**
# 2 - then think of something fancy
# 3 - clean up
# 4 - redefine the web app?
#     - focus only on events (Concerts, games, social vibes?)
#.    - places to watch out? based on number of crimes and police reports?
#     - ano lang ba mga possible mong ma obtain if via web app?
#       - I wanna know the location of? I wanna know the status of location?
#       -

class Recommendation(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        output_parser = StructuredOutputParser.from_response_schemas([
            ResponseSchema(name="latitude", description="latitude"),
            ResponseSchema(name="longitude", description="longitude")
        ])
        self.format_instructions = output_parser.get_format_instructions(only_json=True)

        self.query_template = """
               give me the longitude and latitude of this place {place}, in country {country}.
               always return the result in a json format and no other texts are included in the result.

               Example Result:
               {{
                  \"longitude\": 0.05464003,
                  \"latitude\": 0.023694057
               }}

               {format_instructions}
               """
        self.input_variables = ["country", "place"]
        self.llm_query = LLMQuery(self.query_template, self.input_variables)
        return super(Recommendation, self).dispatch(request, *args, **kwargs)


    def get(self, request, place, category, meters):
        input = {
            'country': 'Philippines',
            'place': place,
            'format_instructions': self.format_instructions
        }
        result = self.llm_query.query(
            input=input
        )

        try:
            data = json.loads(result)

            # need sukatin cosine and euclidean distance from the embedding of this question to some of the actual answers
            # then join to geolocation to include meter distance in the filter
            question = "give me the best hotel based on reviews and feedback provided by customers."
            embedder = get_embedder("HUGGING_FACE")
            embeddings = np.array(embedder.gen_embeddings(question)).tolist()

            # GteSmallWithReviewDate
            results = (
                GteSmallWithReviewDate.objects
                .filter(location__distance_lte=(Point(float(data['longitude']), float(data['latitude'])), D(m=meters)))
                .annotate(distance=CosineDistance("embeddings", embeddings))
                .order_by("distance")[:5]
            )

            serialized_data = GteSmallWithReviewDateSerializer(results, many=True)
            return Response(serialized_data.data, status=status.HTTP_200_OK)

        except json.decoder.JSONDecodeError as e:
            return Response([], status=status.HTTP_503_SERVICE_UNAVAILABLE)


    def post(self, place: str):
        pass



class CoordinateViews(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        output_parser = StructuredOutputParser.from_response_schemas([
            ResponseSchema(name="latitude", description="latitude"),
            ResponseSchema(name="longitude", description="longitude")
        ])
        self.format_instructions = output_parser.get_format_instructions(only_json=True)

        self.query_template = """
        give me the longitude and latitude of this place {place}, in country {country}.
        always return the result only in a json format and no other text are included in the result.
        
        Example Result:
        {{
           \"longitude\": 0.05464003,
           \"latitude\": 0.023694057
        }}
        
        {format_instructions}
        """
        self.input_variables = ["country", "place"]
        self.llm_query = LLMQuery(self.query_template, self.input_variables)
        return super(CoordinateViews, self).dispatch(request, *args, **kwargs)

    def get(self, request, place, location_type, meters):
        input = {
            'country': 'Philippines',
            'place': place,
            'format_instructions': self.format_instructions
        }
        result = self.llm_query.query(
            input=input
        )

        # *********
        # to get an estimation of how many people are present in a place
        # I need to have people to download my app (via mobile), will be extra difficult if it's a web app (cause they need to access the site for us to get geo location)
        # even if we convert to mobile app, how can we get people to download the app.
        # need to deal with GDPR as well, since we'll be tracking people's locations

        # re-think the geo app, still geo related but make it in more feasible way (via web).
        # maybe renaming as vibe checker site. where I can recommend top places in the users current location?
        # *********

        try:
            data = json.loads(result)
            print(data)
            nearby_locations = (GeoLocation.objects.filter(name__isnull=False)
                                .filter(geometry__distance_lte=(Point(float(data['longitude']), float(data['latitude'])), D(m=meters)))
                                .filter(location_class=location_type.strip())
                                )


            serialized_geo = GeoLocationSerializer(nearby_locations, many=True)
            return Response(serialized_geo.data, status=status.HTTP_200_OK)

        except json.decoder.JSONDecodeError as e:
            return Response([], status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # print(data)


        # return Response(serialized_geo.data, status=status.HTTP_200_OK)

        # geo = GeoLocation.objects.all()
        # serialized_geo = GeoLocationSerializer(geo, many=True)

        # reference_point = Point(120.9953, 14.6015, srid=4326)

        # point_data = {'longitude':reference_point.x,'latitude':reference_point.y}




        # nearby_locations = GeoLocation.objects.filter(
        #     geometry__distance_lte=(reference_point, D(m=2000))
        # )
        # nearby_locations = GeoLocation.objects.filter(geometry__distance_lte=(Point( 120.9953, 14.6015), D(m=1000)))
                            # .values('geometry'))



        # locations_data = list(nearby_locations.values('name', 'geometry'))
        # return JsonResponse({'locations': locations_data})

        # SELECT * FROM
        # GeoLocation
        # WHERE
        # ST_Distance_Sphere(geometry, ST_MakePoint(-73.9857, 40.7484)) <= 1000;

    def post(self, request):
        pass


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
