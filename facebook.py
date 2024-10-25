from flask import Flask, redirect, request, jsonify
from requests_oauthlib import OAuth2Session
from facebook import GraphAPI

# Facebook App Credentials
FB_CLIENT_ID = 'your_facebook_app_id'  # Replace with your Facebook App ID
FB_CLIENT_SECRET = 'your_facebook_app_secret'  # Replace with your Facebook App Secret
FB_REDIRECT_URI = 'https://your-redirect-url.com/'  # Replace with your redirect URL
FB_AUTH_BASE_URL = 'https://www.facebook.com/dialog/oauth'
FB_TOKEN_URL = 'https://graph.facebook.com/v14.0/oauth/access_token'

app = Flask(__name__)

@app.route("/login")
def login():
    facebook = OAuth2Session(FB_CLIENT_ID, redirect_uri=FB_REDIRECT_URI, scope=["email", "public_profile", "user_friends"])
    authorization_url, state = facebook.authorization_url(FB_AUTH_BASE_URL)
    
    # Redirect to Facebook login page
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    facebook = OAuth2Session(FB_CLIENT_ID, redirect_uri=FB_REDIRECT_URI)
    # Get the access token
    facebook.fetch_token(FB_TOKEN_URL, client_secret=FB_CLIENT_SECRET, authorization_response=request.url)
    
    # Store access token for future use
    access_token = facebook.token['access_token']
    
    # Fetch profile and friend list data
    return redirect(f"/get_facebook_data?access_token={access_token}")
    

@app.route("/get_facebook_data")
def get_facebook_data():
    access_token = request.args.get('access_token')
    graph = GraphAPI(access_token)
    
    # Fetch profile information
    profile = graph.get_object('me', fields='id,name,email')
    
    # Fetch friend list
    friends = graph.get_connections('me', 'friends')
    
    # Return data as JSON
    return jsonify({
        "profile": profile,
        "friends": friends
    })

if __name__ == "__main__":
    app.run(debug=True)
