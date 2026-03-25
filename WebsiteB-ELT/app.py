from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to the ELT database
    conn = sqlite3.connect('crypto_elt.db')
    cursor = conn.cursor()
    # Query the SQL View, not the raw table!
    cursor.execute("SELECT * FROM crypto_analytics ORDER BY id DESC LIMIT 10")
    data = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', prices=data)

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Port 5001 so it doesn't conflict