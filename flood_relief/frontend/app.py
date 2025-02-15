from flask import Flask, render_template, request, flash, redirect, url_for
import requests
from enum import Enum

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

BACKEND_URL = "http://localhost:8000"  # Adjust this to your backend URL

class ResourceType(str, Enum):
    BOAT = "boat"
    SHELTER = "shelter"
    FOOD = "food"

@app.route('/')
def index():
    # Fetch current demands from the backend
    try:
        response = requests.get(f"{BACKEND_URL}/demands/")
        demands = response.json() if response.status_code == 200 else []
    except requests.RequestException:
        demands = []
        flash("Could not fetch current demands", "error")
    
    return render_template('index.html', demands=demands, resource_types=ResourceType)

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
