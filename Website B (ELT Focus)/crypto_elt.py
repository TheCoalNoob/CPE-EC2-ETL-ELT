# In this script, Python acts only as a courier. It fetches the data and immediately dumps the raw, 
# unedited JSON string into SQLite. We then use an SQL VIEW to extract the values and calculate 
# the PHP prices on the fly whenever the database is queried.
import sqlite3
import requests
import json
from datetime import datetime

URL = "https://api.coingecko.com/api/v3/simple/price"
DB_NAME = "crypto_elt.db"

# --------------------
# DATABASE & TRANSFORM SETUP
# --------------------
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        # 1. The Landing Zone (Raw unedited data)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS raw_crypto_dump (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raw_json TEXT,
                ingested_at TEXT
            )
        """)
        
        # 2. The Transformation Engine (SQL View does the math)
        conn.execute("DROP VIEW IF EXISTS crypto_analytics")
        conn.execute("""
            CREATE VIEW crypto_analytics AS
            SELECT 
                id,
                json_extract(raw_json, '$.bitcoin.usd') AS btc_usd,
                (json_extract(raw_json, '$.bitcoin.usd') * 56.0) AS btc_php,
                json_extract(raw_json, '$.ethereum.usd') AS eth_usd,
                (json_extract(raw_json, '$.ethereum.usd') * 56.0) AS eth_php,
                ingested_at
            FROM raw_crypto_dump
        """)

# --------------------
# EXTRACT
# --------------------
def extract():
    params = {"ids": "bitcoin,ethereum", "vs_currencies": "usd"}
    r = requests.get(URL, params=params)
    r.raise_for_status()
    return r.json()

# --------------------
# LOAD (Raw Dump - No Python Logic)
# --------------------
def load_raw(raw_data):
    # Convert the Python dictionary back into a raw JSON string
    json_str = json.dumps(raw_data)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO raw_crypto_dump (raw_json, ingested_at)
            VALUES (?, ?)
        """, (json_str, timestamp))
        conn.commit()
        print("ELT Pipeline: Raw JSON loaded. The SQL View handles the transformation!")

if __name__ == "__main__":
    init_db()
    raw_data = extract()
    load_raw(raw_data)
