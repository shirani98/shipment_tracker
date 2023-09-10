# tracker/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Shipment
from .serializers import ShipmentSerializer
from .utils import get_weather_data


class ShipmentWeatherView(APIView):
    def get(self, request):
        tracking_number = request.query_params.get("tracking_number")
        carrier = request.query_params.get("carrier")

        # Initialize queryset based on provided query parameters
        queryset = Shipment.objects.all()

        if tracking_number:
            queryset = queryset.filter(tracking_number=tracking_number)
        elif carrier:
            queryset = queryset.filter(carrier=carrier)
        else:
            return Response(
                {"error": "Please provide tracking_number or carrier."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Serialize the matching shipments and include weather data for each
        shipments = queryset.all()
        serializer = ShipmentSerializer(shipments, many=True)
        data = serializer.data

        for shipment_data in data:
            # Get weather data using the receiver's zip code (adjust the field name as needed)
            zip_code = shipment_data["receiver_zip_code"]
            weather_data = get_weather_data(zip_code)

            if weather_data:
                shipment_data["weather_temp"] = weather_data

        return Response(data, status=status.HTTP_200_OK)
