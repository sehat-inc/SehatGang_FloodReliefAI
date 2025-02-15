from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from math import radians, sin, cos, sqrt, atan2

async def get_coordinates(city_name: str) -> tuple[float, float]:
    """Convert city name to coordinates using geocoding"""
    try:
        geolocator = Nominatim(user_agent="flood_relief_app")
        location = geolocator.geocode(city_name)
        if location:
            print(location)
            print("Latitude and Longitude of city:", location.latitude, location.longitude)
            return location.longitude, location.latitude
        raise ValueError(f"Could not find coordinates for city: {city_name}")
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        raise ValueError(f"Geocoding service error: {str(e)}")

def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great-circle distance (in km) between two points
    using their latitude and longitude in decimal degrees.
    """
    # Convert degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    # Earth radius in kilometers
    return 6371 * c