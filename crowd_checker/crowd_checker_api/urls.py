from django.urls import path
from .views import establishments, EstablishmentStatusView, CoordinateViews, Recommendation

urlpatterns = [
    path("establishments/", establishments, name="establishments"),
    path("establishments-status/", EstablishmentStatusView.as_view(), name="establishments_status"),
    path("get-locations/<str:place>/type/<str:location_type>/meters/<int:meters>", CoordinateViews.as_view(), name="coordinates"),
    path("get-recommendations/<str:place>/category/<str:category>/meters/<int:meters>", Recommendation.as_view(), name="recommendations")
]