from django.urls import path
from .views import establishments

urlpatterns = [
    path("establishments/", establishments, name="establishments")
]