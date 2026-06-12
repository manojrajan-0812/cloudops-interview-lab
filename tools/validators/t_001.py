"""T-001: Terraform plan must not show destroy+recreate on every run."""
from tools.lib import read_file, ok, fail
import re


def validate():
    try:
        content = read_file("terraform/main.tf")
    except Exception as e:
        return fail(f"❌ Could not read terraform/main.tf: {e}")

    # Check for timestamp() trigger — the root cause
    if re.search(r'timestamp\s*\(\s*\)', content):
        return fail(
            "❌ terraform/main.tf uses timestamp() as a trigger value.\n"
            "timestamp() is re-evaluated on every plan, causing destroy+recreate every time.\n"
            "Replace with a stable value (e.g. var.app_version or var.environment)."
        )

    # Check the null_resource still exists (removing it entirely is a wrong fix)
    if not re.search(r'resource\s+"null_resource"', content):
        return fail(
            "❌ The null_resource.deployment resource was removed.\n"
            "The correct fix is to replace the volatile trigger, not remove the resource.\n"
            "Restore the null_resource with a stable trigger."
        )

    return ok("null_resource trigger does not use timestamp() — plan will be stable.")
