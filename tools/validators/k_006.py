"""K-006: A PodDisruptionBudget must exist with minAvailable >= 1."""
from tools.lib import load_yaml_all, REPO_ROOT, ok, fail
from pathlib import Path


def validate():
    pdb_path = REPO_ROOT / "k8s" / "pdb.yaml"
    if not pdb_path.exists():
        return fail("❌ k8s/pdb.yaml does not exist. Create a PodDisruptionBudget.")

    try:
        docs = load_yaml_all("k8s/pdb.yaml")
    except Exception as e:
        return fail(f"❌ Could not parse k8s/pdb.yaml: {e}")

    pdbs = [d for d in docs if d and d.get("kind") == "PodDisruptionBudget"]
    if not pdbs:
        return fail(
            "❌ k8s/pdb.yaml exists but contains no PodDisruptionBudget resource.\n"
            "Add a PodDisruptionBudget with kind: PodDisruptionBudget."
        )

    pdb = pdbs[0]
    spec = pdb.get("spec", {})
    min_available = spec.get("minAvailable")
    max_unavailable = spec.get("maxUnavailable")

    if min_available is None and max_unavailable is None:
        return fail(
            "❌ PodDisruptionBudget has neither minAvailable nor maxUnavailable.\n"
            "Add 'minAvailable: 1' to the spec."
        )

    selector = spec.get("selector", {}).get("matchLabels", {})
    if not selector:
        return fail(
            "❌ PodDisruptionBudget has no selector.matchLabels.\n"
            "Add selector.matchLabels.app: interview-api to target the correct pods."
        )

    if min_available is not None:
        try:
            if int(str(min_available)) < 1:
                return fail(f"❌ minAvailable is {min_available} — must be at least 1.")
        except ValueError:
            return fail(
                f"❌ minAvailable value '{min_available}' is not a valid integer.\n"
                "Use a whole number (e.g. minAvailable: 1), not a percentage."
            )

    return ok(f"PodDisruptionBudget exists with minAvailable={min_available}, selector={selector}.")
