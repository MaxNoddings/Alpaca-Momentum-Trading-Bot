import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ALPACA_API_KEY_ID")
secret_key = os.getenv("ALPACA_SECRET_KEY")

print(f"API Key: {api_key}")
print(f"Secret Key: {secret_key}")

if api_key and secret_key:
    print("API keys loaded successfully!")
else:
    print("API keys NOT loaded. Check .env file and environment variables.")