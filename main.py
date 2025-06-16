from fastapi import FastAPI
import threading
import logging
import time
import datetime
from momentumBot import run_bot

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Bot is running"}

def bot_loop():
    logging.info("Starting momentum bot loop...")
    while True:
        try:
            now = datetime.datetime.now()
            if now.weekday() < 5 and 9 <= now.hour <= 16:  # Market hours only
                run_bot()
            else:
                logging.info("Market closed. Sleeping...")
        except Exception as e:
            logging.error(f"Bot crashed: {e}")
        time.sleep(60)  # Run every 60 seconds

@app.on_event("startup")
def startup_event():
    threading.Thread(target=bot_loop, daemon=True).start()
