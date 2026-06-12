"""K-008: Pod must not run privileged or as root."""
from tools.lib import check_k8s_deployment, ok, fail


def validate():
    try:
        dep = check_k8s_deployment()
    except Exception as e:
        return fail(f"❌ Could not read k8s/deployment.yaml: {e}")

    pod_sec = dep.get("pod_security", {})
    containers = dep.get("containers", [])

    # Check pod-level: must not run as root
    run_as_user = pod_sec.get("runAsUser")
    run_as_non_root = pod_sec.get("runAsNonRoot")

    if run_as_user == 0:
        return fail(
            "❌ Pod securityContext.runAsUser is 0 (root).\n"
            "Set runAsUser to a non-zero value (e.g. 1000) and runAsNonRoot: true."
        )

    if run_as_non_root is False:
        return fail("❌ Pod securityContext.runAsNonRoot is explicitly false.")

    # Check container-level: no privileged
    for c in containers:
        csec = c.get("security", {})
        if csec.get("privileged") is True:
            return fail(
                f"❌ Container '{c['name']}' has securityContext.privileged: true.\n"
                f"Remove 'privileged: true' — the app does not need host-level privileges.\n"
                f"Also add allowPrivilegeEscalation: false and capabilities.drop: [ALL]."
            )
        if csec.get("allowPrivilegeEscalation") is True:
            return fail(
                f"❌ Container '{c['name']}' has allowPrivilegeEscalation: true.\n"
                f"Set allowPrivilegeEscalation: false."
            )
        if csec.get("allowPrivilegeEscalation") is None:
            return fail(
                f"❌ Container '{c['name']}' does not set allowPrivilegeEscalation: false.\n"
                f"Explicitly set it to false to prevent privilege escalation."
            )

    return ok("Pod runs as non-root, without privileges, and with allowPrivilegeEscalation: false.")
