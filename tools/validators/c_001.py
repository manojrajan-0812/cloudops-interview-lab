"""C-001: Production deploy job must require manual approval (when: manual)."""
from tools.lib import load_yaml, ok, fail


def validate():
    try:
        ci = load_yaml("ci/.gitlab-ci.yml")
    except Exception as e:
        return fail(f"❌ Could not parse ci/.gitlab-ci.yml: {e}")

    if "deploy-production" not in ci:
        return fail(
            "❌ 'deploy-production' job not found in ci/.gitlab-ci.yml.\n"
            "Do not remove the job — add 'when: manual' to it."
        )

    job = ci["deploy-production"]
    when = job.get("when")

    if when != "manual":
        return fail(
            f"❌ deploy-production job has 'when: {when or \"on_success (default)\"}' — it will run automatically.\n"
            "Add 'when: manual' to the deploy-production job so it requires explicit approval."
        )

    return ok("deploy-production requires manual approval (when: manual).")
