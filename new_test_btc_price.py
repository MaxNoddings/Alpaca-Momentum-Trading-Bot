import os
import time
from datetime import datetime
from alpaca.data.historical import CryptoHistoricalDataClient # Corrected import
from alpaca.data.requests import CryptoLatestTradeRequest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- NO KEYS ARE NEEDED FOR CRYPTO DATA ---
# The new CryptoHistoricalDataClient doesn't require API keys for public market data.

# Initialize the Crypto Data Client
crypto_client = CryptoHistoricalDataClient()

# Define the symbol and request parameters
symbol = "BTC/USD"
request_params = CryptoLatestTradeRequest(symbol_or_symbols=symbol)


while True:
    try:
        # Fetch the latest trade for the symbol using the correct method
        latest_trade = crypto_client.get_crypto_latest_trade(request_params) # FIX: Changed method name

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # The new library returns a dictionary, so we access the trade data by symbol
        if symbol in latest_trade:
            current_price = latest_trade[symbol].price
            print(f"[{now}] Current {symbol} price: {current_price}")
        else:
            print(f"[{now}] No data returned for {symbol}.")
            
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] Error fetching {symbol} price: {e}")
    
    # Sleep for 2 seconds to respect API limits and avoid spamming
    time.sleep(2)