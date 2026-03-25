# In this script, Python does all the heavy lifting. 
# It fetches the data, calculates the PHP values, 
# and formats everything nicely before it ever touches the database.

import sqlite3
import requests
from datetime import datetime

URL = "https://api.coingecko.com/api/v3/simple/price"
DB_NAME = "crypto_etl.db"
EXCHANGE_RATE = 56.0  # Static rate for simplicity

# --------------------
# EXTRACT
# --------------------
def extract():
    params = {"ids": "bitcoin,ethereum", "vs_currencies": "usd"}
    r = requests.get(URL, params=params)
    r.raise_for_status()
    return r.json()

# --------------------
# TRANSFORM (Python handles the logic)
# --------------------
def transform(raw_data):
    btc_usd = raw_data["bitcoin"]["usd"]
    eth_usd = raw_data["ethereum"]["usd"]
    
    # Math happens HERE, before the database
    btc_php = btc_usd * EXCHANGE_RATE
    eth_php = eth_usd * EXCHANGE_RATE
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (btc_usd, btc_php, eth_usd, eth_php, timestamp)

# --------------------
# LOAD (Structured Data Only)
# --------------------
def load(clean_data):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                btc_usd REAL,
                btc_php REAL,
                eth_usd REAL,
                eth_php REAL,
                ingested_at TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO crypto_prices (btc_usd, btc_php, eth_usd, eth_php, ingested_at)
            VALUES (?, ?, ?, ?, ?)
        """, clean_data)
        conn.commit()
        print("ETL Pipeline: Clean data transformed in Python and loaded!")

if __name__ == "__main__":
    raw_data = extract()
    clean_data = transform(raw_data)
    load(clean_data)
