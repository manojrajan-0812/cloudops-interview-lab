"""K-001: Liveness probe must have sufficient initialDelaySeconds and failureThreshold."""
from tools.lib import check_k8s_deployment, ok, fail


def validate():
    try:
        dep = check_k8s_deployment()
    except Exception as e:
        return fail(f"Could not read k8s/deployment.yaml: {e}")

    containers = dep.get("containers", [])
    if not containers:
        return fail("❌ No containers found in deployment.")

    c = containers[0]
    liveness = c.get("liveness")
    if not liveness:
        return fail(
            "❌ No livenessProbe defined.\n"
            "Removing the probe is not the correct fix — it leaves the pod unmonitored.\n"
            "Instead, increase initialDelaySeconds to give the app time to start."
        )

    delay = liveness.get("initialDelaySeconds", 0)
    threshold = liveness.get("failureThreshold", 1)

    if delay < 30:
        return fail(
            f"❌ livenessProbe.initialDelaySeconds is {delay}.\n"
            f"The app takes ~15s to start — initialDelaySeconds should be >= 30.\n"
            f"Current value means the probe fires before the app is ready."
        )

    if threshold < 3:
        return fail(
            f"❌ livenessProbe.failureThreshold is {threshold}.\n"
            f"A single missed check should not immediately restart the pod.\n"
            f"Set failureThreshold to at least 3."
        )

    return ok(f"Liveness probe has initialDelaySeconds={delay} and failureThreshold={threshold}.")
