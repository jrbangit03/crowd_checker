

import ast
import requests
from dataclasses import dataclass
from typing import Dict
from django.contrib.gis.geos import Point
from typing import List

from .embeddings import ModelEmbeddings
from ..models import Review

BASE_URL = "https://api.foursquare.com/v3"


@dataclass
class Review:
    review_id: str
    fsq_id: str
    name: str
    branch: str
    feedback: str
    location: Point
    embeddings: List

class FourSquare:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = self.__gen_headers__()

    def __gen_headers__(self) -> Dict:
        return {"accept": "application/json",
                "Authorization": self.api_key}

    def extract_fsq_ids(self, longitude: float, latitude: float, radius: int, type: str) -> list[Dict]:
        return [{loc["fsq_id"].strip(): {"name": loc["name"],
                                         "location": loc["geocodes"]["main"],
                                         "address": loc["location"]["formatted_address"]}}
                for loc in self.get_locations(longitude, latitude, radius, type)]

    def get_locations(self, longitude: float, latitude: float, radius: int, type: str):
        params = {
            "query": type,
            "ll": f"{longitude},{latitude}",
            "radius": radius,

        }
        response = requests.get(f"{BASE_URL}/places/search",
                                headers=self.headers,
                                params=params)

        return response.json()['results'] if response.ok else []

    def get_reviews(self, fsq_ids: list[Dict], embedder: ModelEmbeddings, include_rev_date: bool) -> list[Review]:
        reviews = []
        for d in fsq_ids:
            for fsq_id, val in d.items():
                response = requests.get(f"{BASE_URL}/places/{fsq_id}/tips",
                                        headers=self.headers)
                if response.ok:
                    resp = ast.literal_eval(response.text)
                    for data in resp:
                        rev_id = data['id']
                        date_of_rev = data['created_at']
                        rev = data['text'].encode('utf-8', errors='replace').decode('utf-8')

                        text = f"""name: {val["name"]} | branch: {val["address"]} | date: {date_of_rev} | review: {rev}""" \
                            if include_rev_date else f"""name: {val["name"]} | branch: {val["address"]} | review: {rev}"""

                        embeddings = embedder.gen_embeddings(text)
                        longitude = val["location"]["longitude"]
                        latitude = val["location"]["latitude"]

                        reviews.append(Review(review_id=rev_id,
                                              fsq_id=fsq_id,
                                              name=val["name"],
                                              branch=val["address"],
                                              feedback=rev,
                                              location=Point(longitude, latitude),
                                              embeddings=embeddings))
        return reviews

            # pending - pre-load location model using the pre-pop command
            # pending - pre-load reviews model(including embeddings column) using new command
            # pending - ask llm query using embedded data from reviews model
            # pending - compress the vector (encoded) using pytorch in a separate table
