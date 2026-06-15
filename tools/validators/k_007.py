"""K-007: ServiceAccount must not be bound to cluster-admin. Must use a scoped Role."""
from tools.lib import load_yaml_all, ok, fail

SA_NAME = "interview-api-sa"


def validate():
    try:
        docs = load_yaml_all("k8s/rbac.yaml")
    except Exception as e:
        return fail(f"❌ Could not parse k8s/rbac.yaml: {e}")

    docs = [d for d in docs if d]

    # 1. No cluster-admin binding for the SA
    crbs = [d for d in docs if d.get("kind") == "ClusterRoleBinding"]
    for crb in crbs:
        if crb.get("roleRef", {}).get("name") == "cluster-admin":
            for s in crb.get("subjects", []):
                if s.get("name") == SA_NAME:
                    return fail(
                        f"❌ {SA_NAME} is still bound to cluster-admin via ClusterRoleBinding.\n"
                        "Replace with a namespace-scoped Role that only allows:\n"
                        "  apiGroups: [''], resources: ['configmaps'], verbs: ['get','list','watch']"
                    )

    # 2. A namespace-scoped Role exists with non-wildcard verbs and resources
    roles = [d for d in docs if d.get("kind") == "Role"]
    if not roles:
        return fail(
            "❌ No Role found in k8s/rbac.yaml.\n"
            "Create a namespace-scoped Role (not ClusterRole) with limited permissions."
        )

    role_names = set()
    for role in roles:
        role_names.add(role["metadata"]["name"])
        for rule in role.get("rules", []):
            if "*" in rule.get("verbs", []):
                return fail(
                    f"❌ Role '{role['metadata']['name']}' has verbs: ['*'] — still over-privileged.\n"
                    "Restrict to: ['get', 'list', 'watch'] on configmaps only."
                )
            if "*" in rule.get("resources", []):
                return fail(
                    f"❌ Role '{role['metadata']['name']}' has resources: ['*'] — still over-privileged.\n"
                    "Restrict to: ['configmaps'] only."
                )

    # 3. A RoleBinding exists that binds the correct SA to one of the Roles above
    rbs = [d for d in docs if d.get("kind") == "RoleBinding"]
    if not rbs:
        return fail("❌ No RoleBinding found. Create a RoleBinding to connect the ServiceAccount to the Role.")

    for rb in rbs:
        sa_bound = any(s.get("name") == SA_NAME for s in rb.get("subjects", []))
        role_bound = rb.get("roleRef", {}).get("name") in role_names
        if sa_bound and role_bound:
            return ok(
                f"ServiceAccount '{SA_NAME}' is bound to a scoped Role via RoleBinding. "
                "No cluster-admin, non-wildcard verbs and resources."
            )

    return fail(
        f"❌ No RoleBinding connects '{SA_NAME}' to the Role you created.\n"
        "Check that the RoleBinding subjects include interview-api-sa and "
        "roleRef.name matches your Role."
    )
