import requests
import base64
import json
import argparse

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="FatSecret Image Recognition API Client")
    parser.add_argument("image_path", help="Path to the image file (jpg, png, or webp)")
    args = parser.parse_args()

    # API endpoint and authentication
    url = "https://platform.fatsecret.com/rest/image-recognition/v2"
    access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjEwOEFEREZGRjZBNDkxOUFBNDE4QkREQTYwMDcwQzE5NzNDRjMzMUUiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJFSXJkX19ha2tacWtHTDNhWUFjTUdYUFBNeDQifQ.eyJuYmYiOjE3NDgzMTMxMTQsImV4cCI6MTc0ODM5OTUxNCwiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mYXRzZWNyZXQuY29tIiwiYXVkIjoiaW1hZ2UtcmVjb2duaXRpb24iLCJjbGllbnRfaWQiOiI5OTk0YjZmNTEyNDQ0MDJhOGU1NDFkMzNmOTcyYTc0NSIsInNjb3BlIjpbImltYWdlLXJlY29nbml0aW9uIl19.ekHPK6pyRugPics15OaBiChYoMmynqEofmHoCsuMVPCjQSU91SPCP9SRH6a6BxAaRmcy68ySAuqJ8opWXHwIIBsB26xtBNwtIzc8Z2MsT4-pb5eH8VNOjq3dmjF1frwe5JIKm1M0aWwPlYzXtH9KXlKoPgg2BwMe3OEsrIGJDddSDkEvR07XEiXLt7wVCn77261--NQupxIa4CmB_272RS2xxIuevjDf0-TdPNoZjj0wv_Vnz7ACsBd2MOG3pCCzKqCK39mZQxiqkLd03CW761LXa9XOoDX7kV9bnbMjjhL-15Wb31jnYVKvATISzaU_803UsDbad2sDKTQKtstNC-FYgreFtlC9NgvsB-CK6aQ0l-9IqEruLEst7-Jvlls4zHkWmb-ofdQodeK8T-IzCaHM_O9VGGp-C1W39b_O1OCCWJ7hWMB-2bzTDO9mIsjGEvMdfihVP82XD0hshERNaMoqdV1q8e-7GkWF2xx28BDIP5w-ezMk1Srn8UxN3MqBfqUNluupzYdN1H4Ep9GzoZXL2MKbIJSBEkdafDcdoc8nuty9zqAZdxGCBXbrqEz8z38m0wOQ9X8ig078lP-0fGBhROaLjGYiXfGq-tCJdOzA1z2nDLBjtmIUWaZVrhIyzez-H_kv7qmR8UL_5ZCnzO0wvCBCzQLvKXBiArH3eLo"  # Replace with your actual access token

    # Read and encode the image to base64
    try:
        with open(args.image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: Image file not found at {args.image_path}")
        return
    except Exception as e:
        print(f"Error reading image file: {e}")
        return

    # Prepare the request body
    request_body = {
        "image_b64": encoded_image,
        "region": "US",              # Optional: Filter results by region
        "language": "en",           # Optional: Language (requires region)
        "include_food_data": True   # Optional: Include detailed food data
    }

    # Set headers with OAuth 2.0 access token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Make the API call
    try:
        response = requests.post(url, json=request_body, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Define the nutrients to display and their units
        nutrients_to_display = ["calories", "protein", "carbohydrate", "fat", "fiber", "sugar"]
        units = {
            "calories": "kcal",
            "protein": "g",
            "carbohydrate": "g",
            "fat": "g",
            "fiber": "g",
            "sugar": "g"
        }

        # Process the response
        if "food_response" in data:
            print("Detected Foods:")
            for food in data["food_response"]:
                name = food["food_entry_name"]
                eaten = food["eaten"]
                total_metric_amount = eaten["total_metric_amount"]
                metric_description = eaten["metric_description"]
                total_nutritional_content = eaten["total_nutritional_content"]

                # Print food name with total metric amount
                print(f"- {name} ({total_metric_amount} {metric_description}):")

                # Print nutritional information
                for nutrient in nutrients_to_display:
                    value = total_nutritional_content.get(nutrient, "N/A")
                    unit = units.get(nutrient, "")
                    if value != "N/A":
                        print(f"  {nutrient.capitalize()}: {value} {unit}")
                    else:
                        print(f"  {nutrient.capitalize()}: N/A")
        elif "error" in data:
            print(f"API Error: {data['error']['message']} (Code: {data['error']['code']})")
        else:
            print("Unexpected response format:", json.dumps(data, indent=2))

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError:
        print("Error: Invalid JSON response from the API")

if __name__ == "__main__":
    main()