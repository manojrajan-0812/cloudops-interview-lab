import os
import time
import sqlite3
import logging
from flask import Flask, jsonify, request

logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", "/tmp/interview.db")
STARTUP_DELAY = int(os.environ.get("STARTUP_DELAY", "0"))

if STARTUP_DELAY:
    time.sleep(STARTUP_DELAY)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, name TEXT, value TEXT)"
    )
    conn.execute("INSERT OR IGNORE INTO records VALUES (1, 'alpha', 'v1')")
    conn.execute("INSERT OR IGNORE INTO records VALUES (2, 'beta', 'v2')")
    conn.commit()
    conn.close()


try:
    init_db()
except Exception as e:
    logger.error(f"Database init failed: {e}")


@app.route("/")
def index():
    return jsonify({"service": "interview-api", "version": "1.0.0", "status": "running"})


@app.route("/api/data")
def data():
    try:
        conn = get_db()
        rows = conn.execute("SELECT * FROM records").fetchall()
        conn.close()
        return jsonify({"records": [dict(r) for r in rows]})
    except Exception as e:
        return jsonify({"error": "query failed"}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"echo": data})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
