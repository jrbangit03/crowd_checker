from django.urls import path
from .views import establishments, EstablishmentStatusView


# Encapsulation

urlpatterns = [
    path("establishments/", establishments, name="establishments"),
    path("establishments-status/", EstablishmentStatusView.as_view(), name="establishments_status")
]