import os
from alpaca_trade_api.rest import REST, TimeFrame
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
BASE_URL = 'https://paper-api.alpaca.markets'

api = REST(API_KEY, SECRET_KEY, BASE_URL)

symbol = "BTCUSD"

try:
    bars = api.get_bars(symbol, TimeFrame.Minute, limit=1).df
    if not bars.empty:
        current_price = bars['close'].iloc[-1]
        print(f"Current BTCUSD price: {current_price}")
    else:
        print("No data returned for BTCUSD.")
except Exception as e:
    print(f"Error fetching BTCUSD price: {e}")