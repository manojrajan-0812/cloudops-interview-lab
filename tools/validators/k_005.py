"""K-005: /health endpoint must return 503 when DB is unreachable, and 200 when it is reachable."""
import sys
import subprocess
from tools.lib import REPO_ROOT, ok, fail

_TEST_SCRIPT = """
import os, sys, importlib
os.environ["DB_PATH"] = "{db_path}"
sys.path.insert(0, "app")
import app as a
importlib.reload(a)
with a.app.test_client() as c:
    r = c.get("/health")
    print(r.status_code)
"""


def _run_health(db_path):
    result = subprocess.run(
        [sys.executable, "-c", _TEST_SCRIPT.format(db_path=db_path)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode != 0:
        return None, result.stderr.strip()
    return result.stdout.strip(), None


def validate():
    if not (REPO_ROOT / "app" / "app.py").exists():
        return fail("❌ app/app.py not found.")

    # 1. Positive test: valid DB path must return 200
    status, err = _run_health("/tmp/interview_validate_test.db")
    if err:
        return fail(f"❌ Could not run health check test.\nError: {err}\nMake sure Flask is installed.")
    if status != "200":
        return fail(
            f"❌ /health returned {status} with a reachable database (expected 200).\n"
            "The endpoint should return 200 when the database is accessible."
        )

    # 2. Negative test: unreachable DB path must return 503
    status, err = _run_health("/nonexistent/invalid/path/db.sqlite")
    if err:
        return fail(f"❌ Could not run health check test.\nError: {err}")
    if status == "200":
        return fail(
            "❌ /health still returns 200 when the database is unreachable.\n"
            "The endpoint must check the database and return 503 on failure.\n"
            "Review the /health handler in app/app.py."
        )
    if status != "503":
        return fail(f"❌ Unexpected status code: {status}. Expected 503 when DB is unreachable.")

    return ok("/health returns 200 with a reachable DB and 503 when the DB is unreachable.")
