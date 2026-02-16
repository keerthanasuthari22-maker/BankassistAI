
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health Check Passed:", response.json())
            return True
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
        return False

def test_chat():
    try:
        print("Sending chat request...")
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": "Hello, are you working?"},
            timeout=120
        )
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat Request Passed in {duration:.2f}s")
            print("Response:", data.get("response", "No text"))
            return True
        else:
            print(f"❌ Chat Request Failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat Request Error: {e}")
        return False

if __name__ == "__main__":
    if test_health():
        test_chat()
