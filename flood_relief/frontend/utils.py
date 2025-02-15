from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def get_city(lat, lon):
    """Convert coordinates to city name using reverse geocoding."""
    try:
        geolocator = Nominatim(user_agent="flood_relief_app")
        location = geolocator.reverse(f"{lat}, {lon}", language="en")
        if location and location.raw.get("address"):
            address = location.raw["address"]
            
            print(f'address1: {address}')
            # Try different address components in order of preference
            return (address.get("city") or 
                   address.get("town") or 
                   address.get("village") or 
                   address.get("suburb") or 
                   address.get("district") or 
                   address)
        
        print(f'address2: {address}')
        return address
    except (GeocoderTimedOut, GeocoderUnavailable, Exception) as e:
        print(f"Geocoding error: {str(e)}")
        print(f'address3: {address}')
        return "Unknown"
