import requests
import json

def test_backend():
    # Test URL
    base_url = "http://127.0.0.1:5000"
    
    # Test data
    test_data = {
        "url": "https://www.amazon.com/product-review/B07ZPKN6YR",
        "reviews": ["This product is amazing! I love it so much. The quality is excellent and it works perfectly."]
    }
    
    print("Testing backend endpoints...")
    
    # Test home endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"Home endpoint status: {response.status_code}")
    except Exception as e:
        print(f"Error testing home endpoint: {e}")
    
    # Test detect endpoint
    try:
        response = requests.get(f"{base_url}/detect")
        print(f"Detect endpoint status: {response.status_code}")
    except Exception as e:
        print(f"Error testing detect endpoint: {e}")
    
    # Test analyze endpoint
    try:
        response = requests.post(
            f"{base_url}/analyze",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Analyze endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("Analysis result:", json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error testing analyze endpoint: {e}")
    
    # Test history endpoint
    try:
        response = requests.get(f"{base_url}/history")
        print(f"History endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("History result:", json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error testing history endpoint: {e}")

if __name__ == "__main__":
    test_backend() 