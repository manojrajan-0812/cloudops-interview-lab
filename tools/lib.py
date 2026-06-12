"""Shared validation helpers for the CloudOps Interview Lab."""

import subprocess
import os
import sys
import yaml
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()


def run(cmd, cwd=None, capture=True, timeout=30):
    """Run a shell command. Returns (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or REPO_ROOT,
        capture_output=capture, text=True, timeout=timeout
    )
    return result.returncode, result.stdout, result.stderr


def load_yaml(path):
    """Load a YAML file relative to REPO_ROOT."""
    full = REPO_ROOT / path
    with open(full) as f:
        return yaml.safe_load(f)


def load_yaml_all(path):
    """Load a multi-document YAML file."""
    full = REPO_ROOT / path
    with open(full) as f:
        return list(yaml.safe_load_all(f))


def read_file(path):
    """Read a file relative to REPO_ROOT."""
    return (REPO_ROOT / path).read_text()


def grep(pattern, path):
    """Return True if regex pattern matches anywhere in file."""
    content = read_file(path)
    return bool(re.search(pattern, content))


def check_dockerfile(path="docker/Dockerfile"):
    """Parse a Dockerfile and return a dict of key properties."""
    content = read_file(path)
    lines = content.splitlines()
    result = {
        "from_tag": None,
        "has_user": False,
        "user_is_root": False,
        "env_vars": [],
        "arg_vars": [],
    }
    for line in lines:
        line = line.strip()
        m = re.match(r'^FROM\s+\S+:(\S+)', line, re.IGNORECASE)
        if m:
            result["from_tag"] = m.group(1).lower()
        if re.match(r'^USER\s+', line, re.IGNORECASE):
            result["has_user"] = True
            user_val = line.split()[1].lower()
            result["user_is_root"] = user_val in ("root", "0")
        m = re.match(r'^ENV\s+(\w+)', line, re.IGNORECASE)
        if m:
            result["env_vars"].append(m.group(1))
        m = re.match(r'^ARG\s+(\w+)', line, re.IGNORECASE)
        if m:
            result["arg_vars"].append(m.group(1))
    return result


def check_k8s_deployment(path="k8s/deployment.yaml"):
    """Parse a k8s Deployment and return a dict of key properties."""
    doc = load_yaml(path)
    containers = doc.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])
    pod_sec = doc.get("spec", {}).get("template", {}).get("spec", {}).get("securityContext", {})
    result = {
        "labels": doc.get("spec", {}).get("template", {}).get("metadata", {}).get("labels", {}),
        "containers": [],
        "pod_security": pod_sec,
    }
    for c in containers:
        result["containers"].append({
            "name": c.get("name"),
            "resources": c.get("resources"),
            "liveness": c.get("livenessProbe"),
            "readiness": c.get("readinessProbe"),
            "security": c.get("securityContext", {}),
        })
    return result


def check_k8s_service(path="k8s/service.yaml"):
    doc = load_yaml(path)
    return {
        "selector": doc.get("spec", {}).get("selector", {}),
        "ports": doc.get("spec", {}).get("ports", []),
    }


def check_prometheus_rules(path="monitoring/prometheus-rules.yaml"):
    doc = load_yaml(path)
    rules = []
    for group in doc.get("groups", []):
        for rule in group.get("rules", []):
            if "alert" in rule:
                rules.append({
                    "name": rule["alert"],
                    "expr": rule.get("expr", ""),
                    "for": rule.get("for", None),
                    "labels": rule.get("labels", {}),
                })
    return rules


def ok(msg=""):
    return True, msg or "✅ Validation passed."


def fail(msg):
    return False, msg
