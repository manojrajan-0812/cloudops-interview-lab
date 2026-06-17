# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

An AI-assisted hands-on interview platform for CloudOps/DevOps/SRE candidates. Candidates get 12 minutes to fix 5 randomly assigned broken production-style configurations. The exercise evaluates both engineering judgment and quality of AI tool usage.

## Auto-loaded Files

@interview
@tools/lib.py

## Common Commands

**Interview runner (main CLI):**
```bash
./interview start --level mid      # mid | senior
./interview validate               # check current fix
./interview next                   # advance to next problem
./interview status                 # show progress
./interview list                   # list all problems
./interview reset                  # reset for next candidate (git reset --hard to baseline_sha)
```

**Flask API:**
```bash
python3 app/app.py                 # runs on 0.0.0.0:8080
```

**Tests:**
```bash
pytest app/tests/ -v
pytest app/tests/test_app.py::test_health_ok -v
pytest app/tests/test_app.py -k "health" -v
```

**Run a single validator directly:**
```bash
python3 -c "from tools.validators.k_001 import validate; passed, msg = validate(); print(msg); exit(0 if passed else 1)"
```

**Install dependencies:**
```bash
pip3 install pyyaml flask structlog prometheus-client pytest
```

## Architecture

### Core Flow

1. `./interview start` picks problems, copies broken files from `problems/{ID}/` into working locations, and **commits that broken state to git** (so `git restore` returns to broken — not clean — state).
2. Candidate edits files in-place.
3. `./interview validate` runs the problem-specific validator in `tools/validators/{id}.py`.
4. Validators check actual behavior/structure (not file diffs) using helpers in `tools/lib.py`.
5. `./interview reset` runs `git reset --hard <baseline_sha>` stored in `.interview-state`.

### Key Components

| Component | Location | Purpose |
|---|---|---|
| Interview runner | `interview` | CLI orchestrating state, problem selection, validation |
| Flask API | `app/app.py` | Central service: `/`, `/api/data`, `/health`, `/metrics`, `/api/echo` |
| Problem bank | `problems/{ID}/` | 15 broken configs + `problem.yaml` (statement, hints, rubric signals) |
| Validators | `tools/validators/*.py` | Per-problem correctness checks |
| Shared helpers | `tools/lib.py` | YAML parsing, Dockerfile/K8s field checks reused across validators |
| Kubernetes baseline | `k8s/*.yaml` | Working manifests (Deployment, Service, Ingress, ConfigMap, Secret, RBAC, PDB) |
| Docker baseline | `docker/Dockerfile` | Working image (pinned version, non-root, multi-stage) |
| Terraform | `terraform/main.tf` | Working IaC (stable keepers, GCS backend) |
| CI/CD | `ci/.gitlab-ci.yml` | GitLab pipeline (test → build → staging → production with manual gate) |
| Monitoring | `monitoring/prometheus-rules.yaml` | Prometheus alert rules |
| State file | `.interview-state` | JSON tracking candidate, queue, current index, baseline SHA, solved set |

### Problem Bank (15 total)

**Mid-level (7):** D-001, K-001, K-002, K-003, K-004, T-001, M-001

**Senior-level (8):** D-002, K-005, K-006, K-007, K-008, K-009, T-002, C-001

**Senior interview composition:** 3 senior + 2 mid problems (enforced by runner).

**Claude traps (senior-only):** K-005 (`/health` always returns 200 even when DB is down) and D-002 (multi-stage Dockerfile leaks a secret via `ENV`) have plausible-but-wrong fixes that Claude typically suggests — catching these is a scoring signal.

### Interviewer Resources (not visible to candidates)

- `interviewer/rubric.md` — 11 weighted scoring categories
- `interviewer/interviewer-guide.md` — observation tips, green/red flags, follow-up questions
- `interviewer/solutions/` — per-problem solution guides

### Docs

- `README.md` — full candidate and interviewer instructions
- `docs/troubleshooting.md` — setup, session, validator troubleshooting
- `PROMPT.md` — the original AI prompt used to build this project

## Runtime Dependencies

Python 3.9+, Git, SQLite3. Optional: Docker, kubectl, Terraform 1.3+ (required by the corresponding validators).
