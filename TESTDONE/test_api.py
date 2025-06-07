import requests
import json

def test_api():
    # API endpoint
    url = 'http://127.0.0.1:5000/analyze'
    
    # Test reviews
    test_reviews = {
        "reviews": [
            "This product is amazing! I love it so much.",
            "Not satisfied with the quality, very disappointed.",
            "Average product, could be better but not bad.",
            "Excellent service and fast delivery!",
            "Worst experience ever, never buying again."
        ]
    }
    
    try:
        # Send POST request
        print("Sending request to API...")
        response = requests.post(url, json=test_reviews)
        
        # Check if request was successful
        if response.status_code == 200:
            print("\nAPI Response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: Status code {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    test_api() 