from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def get_city(lat, lon):
    """Convert coordinates to city name using reverse geocoding."""
    try:
        geolocator = Nominatim(user_agent="flood_relief_app")
        location = geolocator.reverse(f"{lat}, {lon}", language="en")
        
        if location and hasattr(location, 'raw'):
            address = location.raw.get('address', {})
            # Try different address components in order of preference
            return (address.get('city') or 
                   address.get('town') or 
                   address.get('village') or 
                   address.get('suburb') or 
                   address.get('state') or 
                   address.get('country') or 
                   str(address))  # Convert to string if no specific field found
    except Exception as e:
        print(f"Geocoding error: {str(e)}")
    return "Sukkur"
