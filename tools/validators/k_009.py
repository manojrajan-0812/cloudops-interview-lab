"""K-009: API_KEY must not be in ConfigMap; must be in Secret."""
from tools.lib import load_yaml, ok, fail


def validate():
    try:
        cm = load_yaml("k8s/configmap.yaml")
        secret = load_yaml("k8s/secret.yaml")
    except Exception as e:
        return fail(f"❌ Could not read manifests: {e}")

    cm_data = cm.get("data", {}) or {}
    if "API_KEY" in cm_data:
        return fail(
            "❌ API_KEY is still in k8s/configmap.yaml.\n"
            "ConfigMaps are not encrypted. Move API_KEY to k8s/secret.yaml."
        )

    secret_data = secret.get("data", {}) or {}
    secret_string_data = secret.get("stringData", {}) or {}
    if "API_KEY" not in secret_data and "API_KEY" not in secret_string_data:
        return fail(
            "❌ API_KEY is not in k8s/secret.yaml.\n"
            "Add it under 'data' (base64 encoded) or 'stringData' (plaintext — k8s will encode it)."
        )

    return ok("API_KEY has been removed from ConfigMap and added to Secret.")
