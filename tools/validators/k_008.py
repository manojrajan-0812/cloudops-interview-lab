"""K-008: Pod must not run privileged or as root, and must drop ALL capabilities."""
from tools.lib import check_k8s_deployment, ok, fail


def validate():
    try:
        dep = check_k8s_deployment()
    except Exception as e:
        return fail(f"❌ Could not read k8s/deployment.yaml: {e}")

    pod_sec = dep.get("pod_security", {})
    containers = dep.get("containers", [])

    if pod_sec.get("runAsUser") == 0:
        return fail(
            "❌ Pod securityContext.runAsUser is 0 (root).\n"
            "Set runAsUser to a non-zero value (e.g. 1000) and runAsNonRoot: true."
        )

    if pod_sec.get("runAsNonRoot") is not True:
        return fail(
            "❌ Pod securityContext.runAsNonRoot is not set to true.\n"
            "Set runAsNonRoot: true to prevent the container running as root."
        )

    for c in containers:
        csec = c.get("security", {})
        name = c["name"]

        if csec.get("privileged") is True:
            return fail(
                f"❌ Container '{name}' has securityContext.privileged: true.\n"
                "Remove 'privileged: true' — the app does not need host-level privileges."
            )

        if csec.get("allowPrivilegeEscalation") is not False:
            return fail(
                f"❌ Container '{name}' does not set allowPrivilegeEscalation: false.\n"
                "Explicitly set it to false to prevent privilege escalation."
            )

        drop = [str(cap).upper() for cap in csec.get("capabilities", {}).get("drop", [])]
        if "ALL" not in drop:
            return fail(
                f"❌ Container '{name}' does not drop all Linux capabilities.\n"
                "Add capabilities.drop: [ALL] to the container securityContext."
            )

    return ok("Pod runs as non-root, without privileges, allowPrivilegeEscalation: false, and capabilities.drop: [ALL].")
