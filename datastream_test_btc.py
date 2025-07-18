import os
import asyncio
from datetime import datetime
from alpaca.data.live import CryptoDataStream # Import CryptoDataStream
from alpaca.data.enums import CryptoFeed
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- KEYS ARE NEEDED FOR LIVE DATA STREAMS ---
# While historical data might not need keys, live data streams often do.
# Make sure your .env file has ALPACA_API_KEY and ALPACA_SECRET_KEY
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

if not ALPACA_API_KEY or not ALPACA_SECRET_KEY:
    print("WARNING: ALPACA_API_KEY or ALPACA_SECRET_KEY not found in .env file.")
    print("Live data streams typically require API keys for authentication.")
    print("Using dummy values for now, but real keys are recommended for production.")
    # You might want to exit or handle this more robustly in a real application
    ALPACA_API_KEY = "YOUR_DUMMY_API_KEY"
    ALPACA_SECRET_KEY = "YOUR_DUMMY_SECRET_KEY"


# Initialize the Crypto Data Stream Client
# Pass your API keys here
crypto_stream_client = CryptoDataStream(
    api_key=ALPACA_API_KEY,
    secret_key=ALPACA_SECRET_KEY,
    feed=CryptoFeed.US # Specify the data feed, e.g., CryptoFeed.US for US exchanges
)

# Define the symbol
symbol = "BTC/USD"

# --- Define an asynchronous function to handle incoming trade data ---
async def trade_handler(trade):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Current {trade.symbol} price: {trade.price}")

async def main():
    # Subscribe to trades for the specified symbol
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Subscribing to live trades for {symbol}...")
    crypto_stream_client.subscribe_trades(trade_handler, symbol)

    # Start the stream. This will run indefinitely, pushing data to trade_handler.
    # You generally don't need a `while True` loop around `run()`
    await crypto_stream_client.run()

if __name__ == "__main__":
    # Run the asynchronous main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Live stream stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")