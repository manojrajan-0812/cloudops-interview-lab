# CloudOps Interview Lab

An AI-assisted hands-on interview for CloudOps, DevOps, and SRE candidates.

Candidates are given a laptop with Claude Code pre-configured. They investigate and fix **5 randomly assigned problems** from a bank of 15 realistic production-style issues — in **12 minutes**.

The exercise tests two things simultaneously:
- **Real DevOps/SRE engineering judgment** — can they diagnose a broken Kubernetes probe, a security misconfiguration, or a Terraform footgun?
- **Effective AI tool usage** — do they use Claude to understand and verify, or blindly paste whatever it suggests?

---

## Problem Bank

15 problems across Mid and Senior difficulty:

| ID | Title | Level | Layer |
|---|---|---|---|
| D-001 | Dockerfile uses `latest` base image and runs as root | Mid | Docker |
| D-002 | Multi-stage build leaks secret into runtime image via `ENV` | Senior | Docker |
| K-001 | Liveness probe `initialDelaySeconds=1` causes restart loop | Mid | Kubernetes |
| K-002 | Service selector doesn't match deployment labels — 502s | Mid | Kubernetes |
| K-003 | Deployment missing resource limits — pods OOMKilled | Mid | Kubernetes |
| K-004 | Ingress routes to wrong service port — 503s | Mid | Kubernetes |
| K-005 | `/health` always returns 200 even when DB is down | Senior | App + k8s |
| K-006 | No PodDisruptionBudget — node drain takes down all replicas | Senior | Kubernetes |
| K-007 | ServiceAccount bound to `cluster-admin` — violates least privilege | Senior | RBAC |
| K-008 | Pod runs `privileged: true` as root — unnecessary | Senior | k8s Security |
| K-009 | `API_KEY` stored in ConfigMap instead of Secret | Senior | k8s Security |
| T-001 | Terraform `timestamp()` trigger causes destroy+recreate every plan | Mid | Terraform |
| T-002 | Terraform backend is `local` — no remote state or locking | Senior | Terraform |
| C-001 | CI pipeline auto-deploys to production with no manual gate | Senior | CI/CD |
| M-001 | Prometheus alert fires on a single error — no threshold or `for:` | Mid | Monitoring |

**Senior problems are designed with a "Claude trap"** — Claude will often suggest a plausible-but-wrong fix. A strong candidate catches it. For example, K-005's obvious wrong fix is to add a `/healthz` route that always passes; the correct fix is making `/health` actually check the database.

---

## Setup

### Prerequisites

```bash
python3 --version    # 3.9+
pip3 install pyyaml flask
git --version
```

### Clone and initialise

```bash
git clone https://github.com/manojrajan-0812/cloudops-interview-lab.git
cd cloudops-interview-lab
```

Claude Code should already be installed on the interview laptop and opened in VS Code or the terminal.

---

## Running an Interview

### Interviewer: start the session

```bash
./interview start --level mid      # for Mid-level candidates
./interview start --level senior   # for Senior candidates
```

The candidate sees a welcome message, the 12-minute time limit, and their first problem.

### Candidate: investigate → fix → validate → repeat

```bash
./interview validate     # check if the current fix is correct
./interview next         # move to the next problem (after validating)
./interview status       # show progress and elapsed time
```

### Interviewer: reset for next candidate

```bash
./interview reset        # restores all files to broken baseline, clears session
```

---

## Interview Format (60 min total)

| Phase | Time |
|---|---|
| Intro + repo walkthrough | 10 min |
| Hands-on: 5 problems | **12 min** |
| Candidate explains their fixes | 15 min |
| Operational follow-up discussion | 15 min |
| Scoring | 8 min |

---

## Scoring

10 categories scored 1–5. Key categories are weighted:

- **Troubleshooting & root cause** — 2×
- **Validation discipline** — 2×
- **Claude Code usage quality** — 2×
- **Judgment: right fix vs. convenient fix** — 3× (senior only)

See `interviewer/rubric.md` for the full rubric and `interviewer/interviewer-guide.md` for observation tips, hints, and follow-up questions.

---

## Repository Structure

```
app/                    Flask API (the service the lab is built around)
docker/                 Dockerfiles (working baseline)
k8s/                    Kubernetes manifests (working baseline)
terraform/              Terraform config (working baseline)
ci/                     GitLab CI pipeline
monitoring/             Prometheus alerting rules
scripts/                Shell scripts
runbooks/               Incident response runbook
problems/               15 problem directories — each contains broken file(s) + problem.yaml
tools/validators/       One validator per problem (checks real behavior, not just file changes)
tools/lib.py            Shared YAML/k8s/Dockerfile parsing helpers
interview               Python runner CLI
interviewer/            Rubric, interviewer guide, solution guides (not shown to candidates)
```

---

## How the Runner Works

- The **baseline** (`main` branch) has all files in **working state**.
- When `./interview start` assigns a problem, the runner copies that problem's **broken files** over the working files.
- The candidate fixes the broken files.
- `./interview validate` runs the problem's validator — which checks **actual behavior** (YAML structure, logic, security context fields), not just whether a file changed.
- `./interview reset` runs `git reset --hard` to restore the clean baseline.

---

## Candidate Instructions

> **If you are a candidate:** start here — the interviewer will run `./interview start` and your first problem will appear in the terminal.
>
> Use Claude Code (open in VS Code sidebar or terminal) to help you understand and debug. Read files yourself before applying Claude's suggestions. Always run `./interview validate` after making a fix.
>
> **Do not open the `interviewer/` folder.**

---

## License

MIT
