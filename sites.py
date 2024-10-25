import googlemaps
from flask import Flask, jsonify, request

app = Flask(__name__)

# Google API key (replace with your actual API key)
GOOGLE_API_KEY = 'your_google_api_key'

# Initialize Google Maps client
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)