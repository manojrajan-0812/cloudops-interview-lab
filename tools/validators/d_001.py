"""D-001: Dockerfile must use pinned (non-latest) base image and run as non-root."""
from tools.lib import check_dockerfile, ok, fail


def validate():
    try:
        df = check_dockerfile("docker/Dockerfile")
    except Exception as e:
        return fail(f"Could not read docker/Dockerfile: {e}")

    if df["from_tag"] == "latest":
        return fail(
            "❌ docker/Dockerfile still uses 'FROM python:latest'.\n"
            "Pin the image to a specific version (e.g. python:3.11-slim)."
        )

    if not df["has_user"]:
        return fail(
            "❌ docker/Dockerfile has no USER directive.\n"
            "The container will run as root. Add a non-root user before CMD."
        )

    if df["user_is_root"]:
        return fail(
            "❌ docker/Dockerfile has USER root (or USER 0).\n"
            "Switch to a non-root user."
        )

    return ok("Dockerfile uses a pinned base image and runs as a non-root user.")
