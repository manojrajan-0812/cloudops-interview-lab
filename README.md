# CloudOps Interview Lab

Welcome. This lab contains a realistic production-style CloudOps environment with intentional issues introduced for the interview exercise.

**Your goal:** Use Claude Code (already open in the sidebar) and your own engineering knowledge to investigate and fix the assigned problem(s).

---

## How the Interview Works

1. The interviewer will run `./interview start --level mid` or `--level senior`
2. A problem will be displayed in your terminal — read it carefully
3. Investigate the relevant files, use Claude Code to help you reason, and apply a fix
4. Run `./interview validate` to check if your fix is correct
5. When validated, run `./interview next` to proceed
6. You have **15 minutes** total for 5 problems

---

## Commands

```bash
./interview status       # Show current problem and elapsed time
./interview validate     # Check your fix for the current problem
./interview next         # Move to the next problem (after validating)
```

---

## Repository Structure

```
app/              Flask API service (the app the infrastructure serves)
docker/           Dockerfile(s) for building the container image
k8s/              Kubernetes manifests (deployment, service, ingress, RBAC, monitoring)
terraform/        Infrastructure-as-code configuration
ci/               GitLab CI pipeline config
monitoring/       Prometheus alerting rules
scripts/          Operational shell scripts
runbooks/         Incident response runbook
```

---

## How to Use Claude Code

Claude Code is available in the VS Code sidebar. Use it to:

- Understand unfamiliar configuration: *"What does livenessProbe.initialDelaySeconds do?"*
- Investigate files: *"Read k8s/deployment.yaml and explain the probe configuration"*
- Ask for debugging help: *"Why would a pod restart loop occur with this liveness probe?"*
- Review your fix: *"Does this change look correct given the problem description?"*

**Important:**
- Always read the files yourself before applying Claude's suggestions
- Always run `./interview validate` after applying a fix — don't assume Claude is right
- If a fix validates: good. If not: read the failure message, don't just re-ask Claude
- Be ready to explain your root cause analysis and what Claude suggested vs. what you decided

---

## Rules

- Fix only the files relevant to the current problem
- Do not open `interviewer/` — those files are for the interviewer
- Do not commit changes or push to any remote
- Internet access is limited to Claude Code — use it well

---

## After Each Problem

The interviewer will ask you to explain:
1. What was broken and why
2. How you diagnosed it
3. What fix you applied
4. What Claude suggested (if anything) and whether you accepted it
5. What the production impact would have been

---

Good luck — we're looking for real engineering judgment, not perfect answers.
