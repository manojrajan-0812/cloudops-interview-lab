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

    # Check: threshold must not be zero. Extract the numeric value after '>' directly
    # to avoid false-positives from word-boundary matching on decimals like 0.05.
    threshold_match = re.search(r">\s*([\d.]+)", expr)
    if threshold_match:
        if float(threshold_match.group(1)) == 0:
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

    # Check: must be ratio-based. Strip label selectors ({...}) before checking
    # for division to avoid false-positives from slashes in job labels.
    expr_no_labels = re.sub(r"\{[^}]*\}", "", expr)
    if "/" not in expr_no_labels:
        if threshold_match is None or float(threshold_match.group(1)) == 0:
            return fail(
                "❌ The expression should calculate an error ratio, not just a raw count.\n"
                "Example: sum(rate(errors[5m])) / sum(rate(requests[5m])) > 0.05"
            )

    return ok(f"HighErrorRate alert has a meaningful threshold and for: {for_clause}.")
