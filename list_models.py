"""Quick script to list available Gemini models"""
from google import genai
import os

# Load API key
api_key = "AIzaSyBKuDGevTgmjWXipnryYIuuacGtpnXth7I"

client = genai.Client(api_key=api_key)

print("Listing available Gemini models...")
print("="*60)

try:
    models = client.models.list()
    for model in models:
        print(f"\n📍 Model: {model.name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"   Supported methods: {model.supported_generation_methods}")
        if hasattr(model, 'display_name'):
            print(f"   Display name: {model.display_name}")
except Exception as e:
    print(f"Error listing models: {e}")
