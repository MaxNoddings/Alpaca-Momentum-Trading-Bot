import os
import time
import datetime
import logging
import pandas as pd
from alpaca_trade_api.rest import REST, TimeFrame

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
BASE_URL = 'https://paper-api.alpaca.markets'

api = REST(API_KEY, SECRET_KEY, BASE_URL)

def get_signal(symbol):
    bars = api.get_bars(symbol, TimeFrame.Day, limit=15).df
    sma_short = bars['close'].rolling(5).mean().iloc[-1]
    sma_long = bars['close'].rolling(10).mean().iloc[-1]
    if sma_short > sma_long:
        return "buy"
    else:
        return "sell"

def run_bot():
    symbols = ["AAPL", "MSFT", "TSLA"]  # example universe
    for symbol in symbols:
        signal = get_signal(symbol)
        position = None
        try:
            position = api.get_position(symbol)
        except Exception:
            position = None
        now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if signal == "buy" and not position:
            api.submit_order(symbol=symbol, qty=1, side='buy', type='market', time_in_force='day')
            logging.info(f"BUY {symbol}")
        elif signal == "sell" and position:
            api.submit_order(symbol=symbol, qty=1, side='sell', type='market', time_in_force='day')
            logging.info(f"SELL {symbol}")

if __name__ == "__main__":
    logging.info("Starting Alpaca momentum bot...")
    while True:
        try:
            now = datetime.datetime.now()
            logging.info(f"Running the Stockbot Now")
            if now.weekday() < 5 and 9 <= now.hour <= 16:
                run_bot()
            else:
                logging.info("Market is closed. Waiting for next trading day.")
        except Exception as e:
            logging.error(f"Exception occurred: {e}")
        # time.sleep(60 * 1)  # wait 1 min before next run
        time.sleep(15) # try to wait just 15 seconds between runs for testing purposes