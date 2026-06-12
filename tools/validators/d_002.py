"""D-002: Multi-stage Dockerfile must not leak secrets via ENV into runtime image."""
from tools.lib import read_file, ok, fail
import re


def validate():
    try:
        content = read_file("docker/Dockerfile.multistage")
    except Exception as e:
        return fail(f"Could not read docker/Dockerfile.multistage: {e}")

    lines = content.splitlines()
    in_runtime_stage = False
    for line in lines:
        stripped = line.strip()
        # Track which stage we're in (last FROM = runtime)
        if re.match(r'^FROM\s', stripped, re.IGNORECASE):
            in_runtime_stage = True  # each FROM resets; last one is runtime

    # Now re-scan: collect all ENV lines and check they're not setting secret URLs
    # In the BROKEN file, ENV is set before the second FROM (in builder stage)
    # but because ENV persists across stages in single-stage, we check ENV presence
    # The real check: PIP_EXTRA_INDEX_URL should be ARG not ENV
    env_with_secret = re.findall(
        r'^ENV\s+(PIP_EXTRA_INDEX_URL\s*=?\s*\S+)', content, re.MULTILINE | re.IGNORECASE
    )
    if env_with_secret:
        return fail(
            "❌ Dockerfile.multistage uses ENV to set PIP_EXTRA_INDEX_URL.\n"
            "ENV values persist into the runtime image and can be read by anyone with\n"
            "access to the container. Use ARG instead — ARG values do not persist past\n"
            "the build stage."
        )

    # Also verify ARG is used
    if not re.search(r'^ARG\s+PIP_EXTRA_INDEX_URL', content, re.MULTILINE | re.IGNORECASE):
        return fail(
            "❌ PIP_EXTRA_INDEX_URL is neither ENV nor ARG.\n"
            "Add 'ARG PIP_EXTRA_INDEX_URL' before the pip install step in the builder stage."
        )

    return ok("Multi-stage build uses ARG (not ENV) for the private index URL — secret does not leak into runtime image.")
