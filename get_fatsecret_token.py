import requests
import json # For pretty printing the response

# --- CONFIGURATION - FILL THESE IN! ---
ACCESS_TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
# Replace with your actual Client ID and Client Secret
CLIENT_ID = "9994b6f51244402a8e541d33f972a745"
CLIENT_SECRET = "53c8d9284dd2445ea17254e968477762"
# You can change the scope if needed, e.g., "basic premier barcode"
# Ensure your client has access to the requested scopes.
SCOPE = "image-recognition"
# --- END CONFIGURATION ---

def get_access_token():
    """
    Requests an access token from the FatSecret OAuth endpoint.
    """
    if CLIENT_ID == "YOUR_CLIENT_ID" or CLIENT_SECRET == "YOUR_CLIENT_SECRET":
        print("ERROR: Please update CLIENT_ID and CLIENT_SECRET with your actual credentials.")
        return None

    # Data for the POST request body (form-urlencoded)
    data = {
        'grant_type': 'client_credentials',
        'scope': SCOPE
    }

    # HTTP Basic Authentication: (username, password)
    auth = (CLIENT_ID, CLIENT_SECRET)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    print(f"Requesting token from: {ACCESS_TOKEN_URL}")
    print(f"Client ID: {CLIENT_ID}")
    print(f"Scope: {SCOPE}")
    print("---")

    try:
        response = requests.post(ACCESS_TOKEN_URL, data=data, auth=auth, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            print("Successfully retrieved access token!")
            token_data = response.json() # The response is expected to be JSON
            print("\nResponse JSON:")
            print(json.dumps(token_data, indent=2)) # Pretty print the JSON

            # You'll typically want to extract the access_token itself
            access_token = token_data.get('access_token')
            expires_in = token_data.get('expires_in') # Token validity in seconds
            token_type = token_data.get('token_type') # Usually "Bearer"

            print(f"\nAccess Token: {access_token}")
            print(f"Expires In (seconds): {expires_in}")
            print(f"Token Type: {token_type}")

            return access_token
        else:
            print(f"Error getting token. Status Code: {response.status_code}")
            print("Response Text:")
            print(response.text)
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None

if __name__ == "__main__":
    retrieved_token = get_access_token()
    if retrieved_token:
        print("\nToken retrieval successful. You can now use this token for API calls.")
    else:
        print("\nToken retrieval failed.")