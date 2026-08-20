from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres-db")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")


@app.route("/")
def home():
    return jsonify({
        "message": "Hello from Podman Backend!"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "UP"
    })


@app.route("/db")
def database():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()

        cursor.close()
        connection.close()

        return jsonify({
            "database": "PostgreSQL",
            "status": "Connected",
            "version": version[0]
        })

    except Exception as e:
        return jsonify({
            "database": "PostgreSQL",
            "status": "Connection failed",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
