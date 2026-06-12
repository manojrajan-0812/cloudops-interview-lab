"""T-002: Terraform backend must not be 'local'."""
from tools.lib import read_file, ok, fail
import re


def validate():
    try:
        content = read_file("terraform/backend.tf")
    except FileNotFoundError:
        return fail(
            "❌ terraform/backend.tf does not exist.\n"
            "Create a backend.tf with a remote backend (e.g. gcs, s3, azurerm)."
        )
    except Exception as e:
        return fail(f"❌ Could not read terraform/backend.tf: {e}")

    if re.search(r'backend\s+"local"', content):
        return fail(
            "❌ terraform/backend.tf still uses the 'local' backend.\n"
            "Local state is not shared between team members and has no locking.\n"
            "Configure a remote backend (e.g. gcs, s3) with state locking."
        )

    # Verify a real remote backend is configured
    remote_backends = ["gcs", "s3", "azurerm", "remote", "consul", "http", "kubernetes"]
    found = any(re.search(rf'backend\s+"{b}"', content) for b in remote_backends)
    if not found:
        return fail(
            "❌ No recognised remote backend found in terraform/backend.tf.\n"
            f"Use one of: {', '.join(remote_backends)}"
        )

    return ok("Terraform backend is configured for remote state storage (not local).")
