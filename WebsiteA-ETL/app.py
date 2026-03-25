from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to the pre-cleaned ETL database
    conn = sqlite3.connect('crypto_etl.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crypto_prices ORDER BY id DESC LIMIT 10")
    data = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', prices=data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)