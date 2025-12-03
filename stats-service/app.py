from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'postgres-service')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'database')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')

def get_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )

@app.route("/stats", methods=["GET"])
def stats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify({"total_users": count})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
