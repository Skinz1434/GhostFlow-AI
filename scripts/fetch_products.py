import os
import requests

def fetch_product_data():
    # Access the API key from environment variables
    digistore_api_key = os.getenv("DIGISTORE_API_KEY")

    if not digistore_api_key:
        print("API key not found. Please ensure it's set in Secrets.")
        return

    # Example API endpoint - replace with actual endpoint
    api_url = "https://api.digistore.com/v1/products"

    headers = {
        "Authorization": f"Bearer {digistore_api_key}"
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Check for HTTP request errors

        # Assume the response is JSON
        products = response.json()
        print("Products:", products)

    except requests.exceptions.RequestException as e:
        print("Error fetching product data:", e)

if __name__ == "__main__":
    fetch_product_data()