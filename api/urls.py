from .views import ShipmentWeatherView
from django.urls import include, path

urlpatterns = [
    path("shipments/", ShipmentWeatherView.as_view(), name="shipment-weather"),
]
