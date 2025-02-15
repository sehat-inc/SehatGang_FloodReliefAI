from flask import Flask, render_template, request, flash, redirect, url_for
import requests
from enum import Enum
import os

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


app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

BACKEND_URL = "http://localhost:8000"  # Adjust this to your backend URL

class ResourceType(str, Enum):
    BOAT = "boat"
    SHELTER = "shelter"
    FOOD = "food"

@app.route('/')
def index():
    try:
        # Fetch demands
        demands_response = requests.get(f"{BACKEND_URL}/demands/")
        demands = demands_response.json() if demands_response.status_code == 200 else []
        count = len(demands)
        demands = sorted(demands, key=lambda x: x.get('priority', 1), reverse=False)[:]
        
        # Fetch resources
        resources_response = requests.get(f"{BACKEND_URL}/resources/")
        resources = resources_response.json() if resources_response.status_code == 200 else []
        resources = sorted(resources, key=lambda x: x.get('quantity', 0), reverse=True)[:]
        
        # Process cities for both demands and resources
        for item in demands + resources:
            if item.get('location'):
                lat = item['location'].get('latitude')
                lon = item['location'].get('longitude')
                if lat is not None and lon is not None:
                    city = get_city(lat, lon)
                    if city != "Unknown":
                        item['city'] = city
                        
    except requests.RequestException as e:
        print(f"Error fetching data: {str(e)}")
        demands, resources = [], []
        flash("Could not fetch data", "error")
    
    return render_template('index.html', 
                         demands=demands, 
                         resources=resources,
                         resource_types=ResourceType, 
                         count=count)

@app.route('/create_demand', methods=['POST'])
def create_demand():
    try:
        data = {
            "type": request.form['type'],
            "quantity": int(request.form['quantity']),
            "priority": int(request.form['priority']),
            "city": request.form['city']
        }
        
        response = requests.post(f"{BACKEND_URL}/demands/", json=data)
        
        if response.status_code == 200:
            flash("Demand created successfully!", "success")
        else:
            flash(f"Error: {response.json().get('detail', 'Unknown error')}", "error")
            
    except requests.RequestException as e:
        flash(f"Error communicating with backend: {str(e)}", "error")
    except ValueError as e:
        flash(f"Invalid input: {str(e)}", "error")
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)