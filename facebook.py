import requests
from requests_oauthlib import OAuth2Session
from facebook import GraphAPI

# Facebook App Credentials
FB_CLIENT_ID = 'your_facebook_app_id'  # Replace with your Facebook App ID
FB_CLIENT_SECRET = 'your_facebook_app_secret'  # Replace with your Facebook App Secret
FB_REDIRECT_URI = 'https://your-redirect-url.com/'  # Replace with your redirect URL
FB_AUTH_BASE_URL = 'https://www.facebook.com/dialog/oauth'
FB_TOKEN_URL = 'https://graph.facebook.com/v14.0/oauth/access_token'

# Step 1: Facebook OAuth 2.0 Login
def facebook_login():
    facebook = OAuth2Session(FB_CLIENT_ID, redirect_uri=FB_REDIRECT_URI)
    authorization_url, state = facebook.authorization_url(FB_AUTH_BASE_URL, scope=["email", "public_profile", "user_friends"])
    
    print("Visit this URL to login with Facebook:")
    print(authorization_url)

    # Step 2: After user logs in, they will be redirected to the redirect URI
    redirect_response = input("Paste the full redirect URL here: ")
    
    # Step 3: Fetch the Access Token
    facebook.fetch_token(FB_TOKEN_URL, client_secret=FB_CLIENT_SECRET, authorization_response=redirect_response)

    return facebook.token['access_token']

# Step 4: Use Facebook Graph API to get profile info and friend list
def get_facebook_data(access_token):
    # Initialize the Graph API with the access token
    graph = GraphAPI(access_token)
    
    # Fetch profile information
    profile = graph.get_object('me', fields='id,name,email')
    print("Profile Info:", profile)
    
    # Fetch friend list
    friends = graph.get_connections('me', 'friends')
    print("Friend List:", friends)

if __name__ == "__main__":
    # Perform login and get access token
    token = facebook_login()

    # Fetch profile and friend list
    get_facebook_data(token)
