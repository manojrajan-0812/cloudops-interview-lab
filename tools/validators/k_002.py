"""K-002: Service selector must match deployment pod labels."""
from tools.lib import check_k8s_deployment, check_k8s_service, ok, fail


def validate():
    try:
        dep = check_k8s_deployment()
        svc = check_k8s_service()
    except Exception as e:
        return fail(f"Could not read manifests: {e}")

    dep_labels = dep.get("labels", {})
    svc_selector = svc.get("selector", {})

    if not svc_selector:
        return fail("❌ Service has no selector — it will never route to any pod.")

    for key, value in svc_selector.items():
        if dep_labels.get(key) != value:
            return fail(
                f"❌ Service selector '{key}: {value}' does not match deployment label '{key}: {dep_labels.get(key)}'.\n"
                f"The Service cannot find any endpoints.\n"
                f"Align the selector with the deployment's pod template labels."
            )

    return ok(f"Service selector matches deployment labels: {svc_selector}")
