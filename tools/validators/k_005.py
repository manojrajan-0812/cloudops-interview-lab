"""K-005: /health endpoint must return 503 when the database is unreachable."""
import os
import sys
import subprocess
from tools.lib import REPO_ROOT, ok, fail


def validate():
    app_py = REPO_ROOT / "app" / "app.py"
    if not app_py.exists():
        return fail("❌ app/app.py not found.")

    # Run the health check with a bad DB path — should get 503
    test_script = """
import os, sys
os.environ["DB_PATH"] = "/nonexistent/invalid/path/db.sqlite"
sys.path.insert(0, ".")
import importlib
import app as a
importlib.reload(a)
with a.app.test_client() as c:
    r = c.get("/health")
    print(r.status_code)
"""
    result = subprocess.run(
        [sys.executable, "-c", test_script],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=10,
    )

    if result.returncode != 0:
        return fail(
            f"❌ Could not run health check test.\n"
            f"Error: {result.stderr.strip()}\n"
            f"Make sure Flask is installed: pip install flask"
        )

    status_code = result.stdout.strip()
    if status_code == "200":
        return fail(
            "❌ /health still returns 200 when the database is unreachable.\n"
            "The endpoint must check the database and return 503 on failure.\n"
            "Review the /health handler in app/app.py."
        )

    if status_code == "503":
        return ok("/health correctly returns 503 when the database is unreachable.")

    return fail(f"❌ Unexpected status code: {status_code}. Expected 503 when DB is unreachable.")
