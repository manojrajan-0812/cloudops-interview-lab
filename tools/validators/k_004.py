"""K-004: Ingress backend port must match the Service's exposed port."""
from tools.lib import load_yaml, check_k8s_service, ok, fail


def validate():
    try:
        ingress = load_yaml("k8s/ingress.yaml")
        svc = check_k8s_service()
    except Exception as e:
        return fail(f"Could not read manifests: {e}")

    svc_ports = {p["name"]: p["port"] for p in svc.get("ports", [])}
    if not svc_ports:
        return fail("❌ Service has no ports defined.")

    rules = ingress.get("spec", {}).get("rules", [])
    for rule in rules:
        for path in rule.get("http", {}).get("paths", []):
            backend_port = path.get("backend", {}).get("service", {}).get("port", {}).get("number")
            if backend_port is None:
                return fail("❌ Ingress backend has no port number defined.")
            valid_ports = list(svc_ports.values())
            if backend_port not in valid_ports:
                return fail(
                    f"❌ Ingress backend port {backend_port} is not exposed by the Service.\n"
                    f"The Service exposes: {valid_ports}\n"
                    f"The Ingress should reference the Service port, not the container port."
                )

    return ok(f"Ingress backend port correctly references a Service port.")
