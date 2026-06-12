import os
import pytest

os.environ["DB_PATH"] = "/tmp/test_interview.db"

from app import app as flask_app, init_db


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    init_db()
    with flask_app.test_client() as c:
        yield c


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.get_json()["service"] == "interview-api"


def test_data(client):
    r = client.get("/api/data")
    assert r.status_code == 200
    assert len(r.get_json()["records"]) >= 1


def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_health_degraded_when_db_missing(client):
    os.environ["DB_PATH"] = "/nonexistent/path/db.sqlite"
    import importlib, app as a
    importlib.reload(a)
    with a.app.test_client() as c:
        r = c.get("/health")
        assert r.status_code == 503
    os.environ["DB_PATH"] = "/tmp/test_interview.db"
