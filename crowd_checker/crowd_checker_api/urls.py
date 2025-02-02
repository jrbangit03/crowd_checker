from django.urls import path
from .views import get_establishments

urlpatterns = [
    path("establishments/", get_establishments, name="get_establishments")
]