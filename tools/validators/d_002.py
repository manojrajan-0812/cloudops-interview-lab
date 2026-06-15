"""D-002: Multi-stage Dockerfile must use ARG (not ENV) for build-time secrets."""
from tools.lib import read_file, ok, fail
import re


def validate():
    try:
        content = read_file("docker/Dockerfile.multistage")
    except Exception as e:
        return fail(f"Could not read docker/Dockerfile.multistage: {e}")

    # ENV PIP_EXTRA_INDEX_URL bakes the value into the builder image layer.
    # It does NOT carry over to a downstream FROM stage's runtime environment,
    # but it IS visible via docker inspect and docker history on the builder image.
    # ARG is the correct alternative: values are only available during the build step
    # and do not appear in docker inspect output for either stage.
    if re.search(r"^ENV\s+PIP_EXTRA_INDEX_URL", content, re.MULTILINE | re.IGNORECASE):
        return fail(
            "❌ Dockerfile.multistage sets PIP_EXTRA_INDEX_URL with ENV.\n"
            "ENV values are baked into the image layer and visible via docker inspect.\n"
            "Use ARG instead — ARG values are only available during the build step\n"
            "and do not appear in docker inspect output."
        )

    if not re.search(r"^ARG\s+PIP_EXTRA_INDEX_URL", content, re.MULTILINE | re.IGNORECASE):
        return fail(
            "❌ PIP_EXTRA_INDEX_URL is neither ENV nor ARG.\n"
            "Add 'ARG PIP_EXTRA_INDEX_URL' before the pip install step in the builder stage."
        )

    return ok("Multi-stage build uses ARG (not ENV) for the private index URL.")
