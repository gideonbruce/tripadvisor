import googlemaps
from flask import Flask, jsonify, request

app = Flask(__name__)

# Google API key (replace with your actual API key)
GOOGLE_API_KEY = 'your_google_api_key'

# Initialize Google Maps client
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

@app.route("/tourism_sites", methods=["GET"])
def get_tourism_sites():
    location = request.args.get('location')  # Location can be passed as a query parameter
    radius = request.args.get('radius', 5000)  # Optional radius parameter in meters (default is 5km)

    places_result = gmaps.places_nearby(location=location, radius=radius, type='tourist_attraction')
    
    places_data = []
    for place in places_result['results']:
        places_data.append({
            'name': place['name'],
            'location': place['geometry']['location'],
            'address': place.get('vicinity', '')
        })

    return jsonify(places_data)

if __name__ == "__main__":
    app.run(debug=True)
