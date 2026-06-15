import os
import time
import sqlite3
import structlog
from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

log = structlog.get_logger()

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", "/tmp/interview.db")
STARTUP_DELAY = int(os.environ.get("STARTUP_DELAY", "0"))

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP request count",
    ["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["endpoint"],
)

if STARTUP_DELAY:
    log.info("slow_start", delay=STARTUP_DELAY)
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
    log.info("db_init", status="ok")
except Exception as e:
    log.error("db_init_failed", error=str(e))


@app.after_request
def record_metrics(response):
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code,
    ).inc()
    return response


@app.route("/")
def index():
    return jsonify({"service": "interview-api", "version": "1.0.0", "status": "running"})


@app.route("/api/data")
def data():
    with REQUEST_LATENCY.labels(endpoint="/api/data").time():
        try:
            conn = get_db()
            rows = conn.execute("SELECT * FROM records").fetchall()
            conn.close()
            return jsonify({"records": [dict(r) for r in rows]})
        except Exception as e:
            log.error("data_query_failed", error=str(e))
            return jsonify({"error": "query failed"}), 500


@app.route("/health")
def health():
    try:
        conn = get_db()
        conn.execute("SELECT 1")
        conn.close()
        return jsonify({"status": "ok", "db": "connected"}), 200
    except Exception as e:
        log.error("health_check_failed", error=str(e))
        return jsonify({"status": "degraded", "db": "unreachable", "error": str(e)}), 503


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/api/echo", methods=["POST"])
def echo():
    body = request.get_json(silent=True) or {}
    return jsonify({"echo": body})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
