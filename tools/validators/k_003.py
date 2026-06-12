"""K-003: Deployment containers must have both resource requests and limits."""
from tools.lib import check_k8s_deployment, ok, fail


def validate():
    try:
        dep = check_k8s_deployment()
    except Exception as e:
        return fail(f"Could not read k8s/deployment.yaml: {e}")

    containers = dep.get("containers", [])
    if not containers:
        return fail("❌ No containers found.")

    for c in containers:
        res = c.get("resources")
        if not res:
            return fail(
                f"❌ Container '{c['name']}' has no 'resources:' block.\n"
                f"Add both requests and limits for cpu and memory."
            )
        if not res.get("requests"):
            return fail(
                f"❌ Container '{c['name']}' has no resources.requests.\n"
                f"The scheduler cannot plan pod placement without requests."
            )
        if not res.get("limits"):
            return fail(
                f"❌ Container '{c['name']}' has no resources.limits.\n"
                f"Without limits, the pod can consume all node memory and cause OOMKill."
            )
        for field in ("cpu", "memory"):
            if field not in res["requests"]:
                return fail(f"❌ resources.requests.{field} is missing.")
            if field not in res["limits"]:
                return fail(f"❌ resources.limits.{field} is missing.")

    return ok("All containers have cpu and memory requests and limits.")
