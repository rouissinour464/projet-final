
from flask import Flask, request, jsonify
import os
import time
import psycopg2
from psycopg2 import OperationalError, sql

app = Flask(__name__)

# Utiliser les variables d'environnement, avec des valeurs par défaut adaptées au docker-compose
DB_HOST = os.environ.get('DB_HOST', 'postgres')  # <— IMPORTANT: par défaut 'postgres'
DB_PORT = int(os.environ.get('DB_PORT', '5432'))
DB_NAME = os.environ.get('DB_NAME', 'database')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def wait_for_db(max_wait_seconds=60):
    """Attend que PostgreSQL soit prêt à accepter des connexions."""
    start = time.time()
    attempt = 0
    while True:
        try:
            conn = get_connection()
            conn.close()
            print("✅ PostgreSQL est joignable.")
            return
        except OperationalError as e:
            attempt += 1
            elapsed = time.time() - start
            if elapsed > max_wait_seconds:
                print("❌ PostgreSQL indisponible après attente.")
                raise
            sleep_s = min(5 + attempt, 10)  # backoff simple
            print(f"⏳ PostgreSQL pas prêt ({e}). Nouvelle tentative dans {sleep_s}s...")
            time.sleep(sleep_s)

def init_db():
    """Crée la table si elle n'existe pas."""
    wait_for_db()
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        );
    """)
    cur.close()
    conn.close()
    print("✅ Table 'users' vérifiée/créée.")

init_db()

@app.route("/users", methods=["GET"])
def list_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users ORDER BY id DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    users = [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
    return jsonify(users), 200

@app.route("/users", methods=["POST"])
def add_user():
    # Accepter JSON et form-encoded par sécurité
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        # fallback si le frontend envoie du form-data
        data = {
            "name": request.form.get("name"),
            "email": request.form.get("email")
        }

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s);", (name, email))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    # Production: utiliser gunicorn/uwsgi — ici Flask dev server suffit pour test
    app.run(host="0.0.0.0", port=5000)
