from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

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
