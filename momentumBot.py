import os
import datetime
import logging
import pandas as pd
from alpaca_trade_api.rest import REST, TimeFrame

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
BASE_URL = 'https://paper-api.alpaca.markets'

api = REST(API_KEY, SECRET_KEY, BASE_URL)

def get_signal(symbol):
    bars = api.get_bars(symbol, TimeFrame.Day, limit=15).df
    if bars.empty or len(bars) < 10:
        logging.warning(f"Not enough data to calculate signal for {symbol}")
        return "hold"
    sma_short = bars['close'].rolling(5).mean().iloc[-1]
    sma_long = bars['close'].rolling(10).mean().iloc[-1]
    return "buy" if sma_short > sma_long else "sell"

def run_bot():
    symbols = ["AAPL", "MSFT", "TSLA"]
    for symbol in symbols:
        bars = api.get_bars(symbol, TimeFrame.Day, limit=15).df
        if bars.empty or len(bars) < 10:
            logging.warning(f"Not enough data to calculate signal for {symbol}")
            continue

        current_price = bars['close'].iloc[-1]
        sma_short = bars['close'].rolling(5).mean().iloc[-1]
        sma_long = bars['close'].rolling(10).mean().iloc[-1]
        signal = "buy" if sma_short > sma_long else "sell"

        try:
            position = api.get_position(symbol)
        except Exception:
            position = None

        logging.info(f"{symbol} | Current Price: {current_price:.2f} | SMA5: {sma_short:.2f} | SMA10: {sma_long:.2f}")

        if not position:
            # Only log "how far from buy" if no position
            distance = sma_short - sma_long
            logging.info(f"{symbol} | How far from BUY: {distance:.2f} (SMA5 - SMA10)")
        else:
            # Only log "how far from sell" if position exists
            distance = sma_long - sma_short
            logging.info(f"{symbol} | How far from SELL: {distance:.2f} (SMA10 - SMA5)")

        if signal == "buy" and not position:
            api.submit_order(symbol=symbol, qty=1, side='buy', type='market', time_in_force='day')
            logging.info(f"BUY: {symbol}")
        elif signal == "sell" and position:
            api.submit_order(symbol=symbol, qty=1, side='sell', type='market', time_in_force='day')
            logging.info(f"SELL: {symbol}")
