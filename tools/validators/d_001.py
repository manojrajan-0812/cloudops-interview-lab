"""D-001: Dockerfile must use a pinned (specific) base image tag and run as non-root."""
from tools.lib import check_dockerfile, ok, fail
import re


def validate():
    try:
        df = check_dockerfile("docker/Dockerfile")
    except Exception as e:
        return fail(f"Could not read docker/Dockerfile: {e}")

    tag = df["from_tag"]

    if tag is None or tag == "latest":
        return fail(
            "❌ docker/Dockerfile still uses 'FROM python:latest'.\n"
            "Pin the image to a specific version (e.g. python:3.11-slim)."
        )

    # Reject single-component tags like "3" — require at least major.minor (e.g. "3.11" or "3.11-slim")
    numeric_part = tag.split("-")[0]
    if not re.search(r"\d+\.\d+", numeric_part):
        return fail(
            f"❌ docker/Dockerfile uses tag '{tag}' which is not sufficiently pinned.\n"
            "A single major version (e.g. python:3) can change with minor/patch releases.\n"
            "Pin to at least major.minor (e.g. python:3.11-slim)."
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

    return ok(f"Dockerfile uses a pinned base image (:{tag}) and runs as a non-root user.")
