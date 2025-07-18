import os
import asyncio
from datetime import datetime
from alpaca.data.live import CryptoDataStream
from alpaca.data.enums import CryptoFeed
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables using the correct names
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY_ID") # Changed from "API_KEY"
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY") # Changed from "SECRET_KEY"

# Crucial: Check if keys are actually loaded
if not ALPACA_API_KEY or not ALPACA_SECRET_KEY:
    print("Error: ALPACA_API_KEY_ID or ALPACA_SECRET_KEY are not loaded.")
    print("Please ensure your .env file is correctly configured with valid API keys.")
    exit(1) # Exit if keys are missing/invalid, as the stream won't work

# Initialize the Crypto Data Stream Client
crypto_stream_client = CryptoDataStream(
    api_key=ALPACA_API_KEY,
    secret_key=ALPACA_SECRET_KEY,
    feed=CryptoFeed.US
)

symbol = "BTC/USD"

async def trade_handler(trade):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Current {trade.symbol} price: {trade.price}")

async def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Subscribing to live trades for {symbol}...")

    # Subscribe to trades for the specified symbol
    crypto_stream_client.subscribe_trades(trade_handler, symbol)

    # Run the stream. This will block until the stream is stopped.
    await crypto_stream_client.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Live stream stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")