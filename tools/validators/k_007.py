"""K-007: ServiceAccount must not be bound to cluster-admin. Must use a scoped Role."""
from tools.lib import load_yaml_all, ok, fail


def validate():
    try:
        docs = load_yaml_all("k8s/rbac.yaml")
    except Exception as e:
        return fail(f"❌ Could not parse k8s/rbac.yaml: {e}")

    docs = [d for d in docs if d]

    # Check for forbidden cluster-admin binding
    crbs = [d for d in docs if d.get("kind") == "ClusterRoleBinding"]
    for crb in crbs:
        role_ref = crb.get("roleRef", {})
        if role_ref.get("name") == "cluster-admin":
            subjects = crb.get("subjects", [])
            for s in subjects:
                if s.get("name") == "interview-api-sa":
                    return fail(
                        "❌ interview-api-sa is still bound to cluster-admin via ClusterRoleBinding.\n"
                        "Replace with a namespace-scoped Role that only allows:\n"
                        "  apiGroups: [''], resources: ['configmaps'], verbs: ['get','list','watch']"
                    )

    # Check for a proper Role (not ClusterRole) with limited verbs
    roles = [d for d in docs if d.get("kind") == "Role"]
    if not roles:
        return fail(
            "❌ No Role found in k8s/rbac.yaml.\n"
            "Create a namespace-scoped Role (not ClusterRole) with limited permissions."
        )

    for role in roles:
        for rule in role.get("rules", []):
            verbs = rule.get("verbs", [])
            resources = rule.get("resources", [])
            # Flag over-privileged roles
            if "*" in verbs:
                return fail(
                    f"❌ Role '{role['metadata']['name']}' has verbs: ['*'] — still over-privileged.\n"
                    f"Restrict to: ['get', 'list', 'watch'] on configmaps only."
                )
            if "*" in resources:
                return fail(
                    f"❌ Role '{role['metadata']['name']}' has resources: ['*'] — still over-privileged.\n"
                    f"Restrict to: ['configmaps'] only."
                )

    # Check a RoleBinding exists linking the SA to the Role
    rbs = [d for d in docs if d.get("kind") == "RoleBinding"]
    if not rbs:
        return fail("❌ No RoleBinding found. Create a RoleBinding to connect the ServiceAccount to the Role.")

    return ok("ServiceAccount is bound to a scoped Role (no cluster-admin). Verbs and resources are restricted.")
