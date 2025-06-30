import os
import time
from datetime import datetime
from alpaca_trade_api.rest import REST, TimeFrame
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
BASE_URL = 'https://paper-api.alpaca.markets'

# It's a good practice to specify the API version
api = REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

# Use the correct symbol format for Bitcoin
symbol = "BTC/USD"

while True:
    try:
        # Use the dedicated function for cryptocurrency bars for clarity and reliability
        bars = api.get_crypto_bars(symbol, TimeFrame.Minute, limit=1).df

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not bars.empty:
            current_price = bars['close'].iloc[-1]
            print(f"[{now}] Current {symbol} price: {current_price}")
        else:
            print(f"[{now}] No data returned for {symbol}.")
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] Error fetching {symbol} price: {e}")
    time.sleep(15)