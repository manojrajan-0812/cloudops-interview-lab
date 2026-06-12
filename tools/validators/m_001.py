"""M-001: HighErrorRate alert must have a meaningful threshold and 'for:' clause."""
from tools.lib import check_prometheus_rules, ok, fail
import re


def validate():
    try:
        rules = check_prometheus_rules()
    except Exception as e:
        return fail(f"❌ Could not parse monitoring/prometheus-rules.yaml: {e}")

    high_error = next((r for r in rules if r["name"] == "HighErrorRate"), None)
    if not high_error:
        return fail(
            "❌ HighErrorRate alert not found.\n"
            "Do not remove it — fix the expression and add a 'for:' clause."
        )

    expr = high_error.get("expr", "")
    for_clause = high_error.get("for")

    # Check: must not be a simple rate > 0 (zero threshold)
    if re.search(r'>\s*0\b', expr) and "0\." not in expr:
        return fail(
            "❌ HighErrorRate fires when error rate > 0 (any single error triggers it).\n"
            "Use a percentage threshold (e.g. > 0.05) by dividing by total request rate."
        )

    # Check: must have a 'for:' clause
    if not for_clause:
        return fail(
            "❌ HighErrorRate has no 'for:' clause.\n"
            "Without 'for:', the alert pages immediately on the first occurrence.\n"
            "Add 'for: 5m' (or similar) to require the condition to persist."
        )

    # Check: must be ratio-based (contains division) OR has a non-zero numeric threshold
    has_division = "/" in expr
    threshold_match = re.search(r'>\s*([\d.]+)', expr)
    threshold_val = float(threshold_match.group(1)) if threshold_match else 0

    if not has_division and threshold_val == 0:
        return fail(
            "❌ The expression should calculate an error *rate* or *ratio*, not just count.\n"
            "Example: sum(rate(errors[5m])) / sum(rate(requests[5m])) > 0.05"
        )

    return ok(f"HighErrorRate alert has a meaningful threshold and for: {for_clause}.")
