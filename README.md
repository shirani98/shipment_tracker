# Shipment Tracking and Weather API
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Django Version](https://img.shields.io/badge/Django-4.2%2B-green.svg)
![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-3.14%2B-orange.svg)
## Overview

This Django project is designed to provide end-users with the ability to track shipments and obtain current weather conditions at their specified location. It offers a RESTful API for retrieving shipment details and weather data based on tracking numbers and carriers. The project integrates with a weather API service to fetch weather information and caches it to minimize API calls.

## Features

### Shipment Tracking

- **Retrieve Shipments:** Users can query shipments based on tracking numbers or carrier names.

- **Shipment Details:** The API provides shipment details such as tracking number, carrier, sender and receiver addresses, article information (name, quantity, price, SKU), and shipment status.

- **Automated Weather Integration:** Weather data for the receiver's location (determined by zip code) is automatically integrated into the shipment data.

### Weather Integration

- **Current Weather Data:** The system fetches current weather conditions from an external weather API (Weatherbit) based on the receiver's zip code.

- **Weather Data Caching:** To minimize API calls and reduce response times, weather data is cached. Weather information for the same location (zip code) is refreshed at most every 2 hours.

### Data Models

The project includes the following data models:

- **Shipment Model:** Stores shipment information, including tracking number, carrier, sender and receiver addresses, article details, SKU, and status.

- **Weather data:** Stores weather information in Redis cache.


### Clone the Repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/shirani98/shipment_tracker.git
```

### Set Up Environment Variables

1. Create a .env file in the project's root directory.
2. Add your Weather API Key to the .env file as follows:
```bash
WEATHER_API_KEY=your_weather_api_key_here
```
Replace your_weather_api_key_here with your actual Weather API Key.

### Install Dependencies

Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate
```
Install project dependencies:

```bash
pip install -r requirements.txt
```

### Configure Redis
Ensure that Redis is installed and running on your system. Update the CACHES settings in settings.py to point to your Redis instance.


### Run Migrations
Apply database migrations:
```bash
python manage.py migrate
```

### Run the Development Server
Start the Django development server:
```bash
python manage.py runserver
```
The project will be accessible at http://localhost:8000.

### Usage
- **Retrieve shipments by tracking number or carrier:** GET /api/shipments/?tracking_number=TN12345678
- **Retrieve shipments by carrier:** GET /api/shipments/?carrier=DHL



