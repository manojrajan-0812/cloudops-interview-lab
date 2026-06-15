# Build a CloudOps AI-Assisted Interview Lab

> **This is the AI prompt that built this project.**
> It is included here as a reference for team members learning how to write effective prompts for Claude or similar AI coding assistants when designing and building non-trivial projects.
>
> **Reference implementation:** https://github.com/manojrajan-0812/cloudops-interview-lab
>
> **How to use this file:**
> Paste the content from "What You Are Building" onwards into Claude Code and it will rebuild this project from scratch. The prompt works because it combines:
> - Clear constraints (what to build and what not to build)
> - Explicit design rules discovered through iteration (the "Do Not Violate" section)
> - A verification checklist so the AI can confirm the build is correct
>
> The more specific and opinionated your prompt, the better the output. Documenting what failed is as important as documenting what to build.
>
> This document is a complete specification. Build exactly what is described. Do not add features, abstractions, or alternatives beyond what is specified. When in doubt, refer to the reference implementation.

---

## What You Are Building

A hands-on interview lab for CloudOps, DevOps, and SRE candidates. Candidates are given a laptop with Claude Code pre-configured. They investigate and fix **5 randomly assigned problems** from a bank of 15 realistic production-style issues — in **12 minutes**.

The lab tests two things simultaneously:
- **Real DevOps/SRE engineering judgment** — can they diagnose a broken Kubernetes probe, a security misconfiguration, or a Terraform footgun?
- **Effective AI tool usage** — do they use Claude to understand and verify, or blindly paste whatever it suggests?

---

## Hard Constraints

- **15 problems** in the bank
- **5 problems** assigned per candidate session
- **12 minutes total** for all 5 (≈2.4 min per problem)
- **Difficulty: Mid + Senior only** — no Junior tier
- **Local-only** — runs entirely on the interview laptop with no real cloud access
- **Safe and resettable** — `./interview reset` restores the environment completely for the next candidate
- **Self-contained** — no internet access required during the interview (Claude Code is pre-configured)

---

## Repository Location and Structure

Build the repo at the path specified by the user, or default to `~/cloudops-interview-lab`.

```
cloudops-interview-lab/
├── README.md                     # candidate + interviewer entry point
├── setup.sh                      # one-shot install script for a new laptop
├── interview                     # executable Python runner (single file, no framework)
├── app/
│   ├── app.py                    # Flask API using structlog + prometheus_client
│   ├── requirements.txt          # flask, gunicorn, structlog, prometheus-client, pydantic, psycopg2-binary
│   └── tests/test_app.py
├── docker/
│   ├── Dockerfile                # working baseline (pinned tag, non-root user)
│   └── Dockerfile.multistage     # working baseline (ARG not ENV for secrets)
├── k8s/
│   ├── deployment.yaml           # working baseline
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── ingress.yaml
│   ├── rbac.yaml
│   └── pdb.yaml
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── backend.tf
├── ci/.gitlab-ci.yml
├── monitoring/prometheus-rules.yaml
├── scripts/backup.sh
├── runbooks/incident-response.md
├── problems/                     # 15 problem directories
│   └── {ID}/
│       ├── problem.yaml          # metadata + candidate_statement
│       └── {layer}/              # broken file(s) for this problem only
├── tools/
│   ├── lib.py                    # shared YAML/Dockerfile/k8s parsing helpers
│   └── validators/               # one Python module per problem
│       └── {id}.py               # validate() -> (bool, str)
├── interviewer/
│   ├── rubric.md                 # scoring formula, categories, hire thresholds
│   ├── interviewer-guide.md      # observation tips, hints, follow-up questions
│   └── solutions/                # one .md file per problem (root cause, fix, traps)
├── .interview-state              # gitignored session file
└── .gitignore
```

---

## The Sample App

A small Flask API (`app/app.py`) that the lab is built around. It must:

- Use `structlog` for structured JSON logging (not stdlib `logging`)
- Use `prometheus_client` to expose a real `/metrics` endpoint with `Counter` and `Histogram`
- Connect to a SQLite database at `$DB_PATH` (defaults to `/tmp/interview.db`)
- Expose these routes: `GET /`, `GET /health`, `GET /api/data`, `POST /api/echo`, `GET /metrics`
- `/health` must check the database with `SELECT 1` and return 200 if reachable, 503 if not
- Support `STARTUP_DELAY` env var (simulates slow-start for K-001)

`requirements.txt` must include: `flask`, `gunicorn`, `structlog`, `prometheus-client`, `pydantic`, `psycopg2-binary`

---

## The Runner — `./interview`

Single Python 3 file using only stdlib + `pyyaml`. Make it executable (`chmod +x`).

### Commands

| Command | Behaviour |
|---|---|
| `./interview start --level mid\|senior` | Prompts for candidate name → picks 5 problems → writes `.interview-state` → applies first broken fixture → prints welcome + first problem |
| `./interview validate` | Runs current problem's validator → prints ✅ or ❌ with hint (never the answer) → records attempt |
| `./interview next [--force]` | Advances to next problem. Refuses if current not validated. `--force` is interviewer override. After all 5 solved: prints "You have finished... Run reset to restart." |
| `./interview status` | Shows candidate name, level, elapsed time, **remaining time**, progress, problem list |
| `./interview list [--level mid\|senior]` | Lists all problems in the bank with ID, level, title, layer |
| `./interview reset` | `git reset --hard HEAD` + `git clean -fdx` scoped to repo root → deletes `.interview-state` |

### State file `.interview-state` (gitignored JSON)

```json
{
  "candidate": "Sarah Johnson",
  "level": "mid",
  "queue": ["K-001", "D-001", "T-001", "M-001", "K-003"],
  "current_idx": 0,
  "started_at": 1234567890.0,
  "attempts": {"K-001": 2},
  "solved": ["K-001"]
}
```

### Time limit behaviour

`TIME_LIMIT_SECONDS = 720` (12 minutes)

When the **final problem** is validated:
- Under 12 min: `🎉 Congratulations, {name}! You have successfully passed the AI-assisted coding interview.`
- Over 12 min: `⏱ {name}, you have taken {elapsed} to complete the AI-assisted coding interview. The expected time was 12 minutes. Thank you for your attempt — better luck next time.`

### Start message (shown after name prompt)

```
Enter your name: _

============================================================
  All the best, {name}!
  You have 12 minutes to complete the task.
============================================================

  You may take help from any AI assistant:

  Option 1 — Claude (recommended):
    Open a new terminal tab and run:
      cd {REPO_ROOT}
      claude
    Claude will be available to help you.

  Option 2 — Any other AI assistant:
    Open a browser and use any free AI tool,
    e.g. ChatGPT (chatgpt.com) or Gemini (gemini.google.com)

============================================================
```

### Problem display

After each `next` or at `start`, print the problem in this format:

```
============================================================
  Problem N/5  ·  {ID}  ·  [{LEVEL}]
  {title}
============================================================

{candidate_statement}

────────────────────────────────────────────────────────────
```

After a successful validate (not the last problem):
```
▶  Run './interview next' to continue  (N problem(s) remaining)
─────────────────────────────────────────────────
```

### Problem composition rules

- **Mid session:** 5 problems from the mid pool, at least 1 from each of {Docker, k8s, Terraform/CI, Monitoring}
- **Senior session:** 3 Senior + 2 Mid; at least 1 Senior from each of {security/RBAC, reliability, operational risk}
- If the pool is smaller than required, print a warning — never silently return fewer than 5

### How problems are applied

Each `problems/{ID}/` directory contains only the broken file(s) for that problem. When a problem is activated, the runner copies those files into the working tree (overwriting the baseline). The baseline has all files in their **correct working state**. Reset restores the baseline.

---

## Problem Bank — 15 Problems

### Distribution

- **Mid (8):** D-001, K-001, K-002, K-003, K-004, T-001, M-001, and one more Mid
- **Senior (7):** D-002, K-005, K-006, K-007, K-008, K-009, T-002, C-001

### All 15 Problems

| ID | Title | Level | Layer | Broken file(s) |
|---|---|---|---|---|
| D-001 | Dockerfile uses `latest` base image and runs as root | Mid | Docker | `docker/Dockerfile` |
| D-002 | Multi-stage build leaks secret via `ENV` into image layer | Senior | Docker | `docker/Dockerfile.multistage` |
| K-001 | Liveness probe `initialDelaySeconds=1` causes restart loop | Mid | k8s | `k8s/deployment.yaml` |
| K-002 | Service selector doesn't match deployment labels — 502s | Mid | k8s | `k8s/service.yaml` |
| K-003 | Deployment missing resource limits — pods OOMKilled | Mid | k8s | `k8s/deployment.yaml` |
| K-004 | Ingress routes to wrong service port — 503s | Mid | k8s | `k8s/ingress.yaml` + `k8s/service.yaml` |
| K-005 | `/health` always returns 200 even when DB is down | Senior | App + k8s | `app/app.py` |
| K-006 | No PodDisruptionBudget — node drain takes down all replicas | Senior | k8s | `k8s/pdb.yaml` (empty) |
| K-007 | ServiceAccount bound to `cluster-admin` | Senior | k8s RBAC | `k8s/rbac.yaml` |
| K-008 | Pod runs `privileged: true` as root | Senior | k8s security | `k8s/deployment.yaml` |
| K-009 | `API_KEY` stored in ConfigMap instead of Secret | Senior | k8s | `k8s/configmap.yaml` + `k8s/secret.yaml` |
| T-001 | `timestamp()` trigger causes destroy+recreate every plan | Mid | Terraform | `terraform/main.tf` |
| T-002 | Terraform backend is `local` — no remote state or locking | Senior | Terraform | `terraform/backend.tf` |
| C-001 | CI auto-deploys to production with no manual gate | Senior | CI/CD | `ci/.gitlab-ci.yml` |
| M-001 | Prometheus alert fires on a single error — no threshold or `for:` | Mid | Monitoring | `monitoring/prometheus-rules.yaml` |

### Senior "Claude Trap" Design Rule

Every Senior problem must have a **tempting wrong fix that Claude commonly suggests**. The validator must reject this wrong fix. This is the primary signal for senior candidates.

| Problem | Claude's wrong suggestion | Correct fix |
|---|---|---|
| K-005 | Add `/healthz` that always returns 200 | Fix `/health` to actually check the DB |
| K-006 | Increase `maxSurge` in rollingUpdate | Add a `PodDisruptionBudget` with `minAvailable: 1` |
| K-007 | Create a Role with `verbs: ["*"]` | Scope verbs to `["get","list","watch"]` on configmaps only |
| K-008 | Only set `runAsNonRoot: true` | Also remove `privileged: true` and add `allowPrivilegeEscalation: false` + `capabilities.drop: [ALL]` |
| T-002 | Run `terraform state push` before reinitialising | Run `terraform init -migrate-state` |
| D-002 | Move `ENV` to the runtime stage | Change `ENV` to `ARG` in the builder stage |

### Problem YAML Schema

```yaml
id: K-001
title: "Liveness probe causes restart loop on slow-starting pod"
level: mid
layer: kubernetes
files_in_play:
  - k8s/deployment.yaml
candidate_statement: |
  The interview-api deployment keeps restarting. Pods briefly appear Running
  but are killed before they finish starting up. The application log shows
  it takes about 15 seconds to initialise.

  Investigate k8s/deployment.yaml and fix the probe configuration.
  Validate with: ./interview validate
hints_interviewer_only:
  - livenessProbe.initialDelaySeconds is 1; app needs 15s to start
  - failureThreshold is 1; one miss = restart
  - Fix: initialDelaySeconds >= 30, failureThreshold >= 3
expected_fix_summary: "Raise initialDelaySeconds to >= 30 and failureThreshold to >= 3"
common_wrong_fixes:
  - Removing the livenessProbe entirely (unsafe; validator rejects)
  - Fixing readinessProbe instead of livenessProbe
follow_ups:
  - What is the difference between liveness and readiness probes?
  - What happens if you remove the liveness probe entirely?
rubric_signals: [kubernetes_understanding, troubleshooting_root_cause, validation_discipline]
```

---

## Validation Framework

### Core rules (never break these)

1. **Validators never check whether a file changed** — they check actual behavior (parsed YAML fields, logic, file content semantics)
2. **Each problem fixture must be self-contained** — if the validator reads file X, the problem directory must include file X
3. **Validators return `(bool, str)`** — the string is candidate-safe (hints without spoilers)
4. **K-005 validator must test both directions** — positive test (reachable DB → 200) AND negative test (unreachable DB → 503). One-directional testing allows `return 503` unconditionally to pass

### What each validator checks

| Problem | What the validator checks |
|---|---|
| D-001 | `FROM` tag is not `latest` and contains `major.minor`; `USER` directive exists and is not root |
| D-002 | No `ENV PIP_EXTRA_INDEX_URL` line; `ARG PIP_EXTRA_INDEX_URL` is present |
| K-001 | `livenessProbe.initialDelaySeconds >= 30`; `failureThreshold >= 3`; probe not removed |
| K-002 | `service.selector` matches `deployment.template.labels` |
| K-003 | All containers have `resources.requests` AND `resources.limits` for both `cpu` and `memory` |
| K-004 | Ingress backend port matches a port exposed by the Service |
| K-005 | Subprocess test: `/health` with valid DB → 200; with invalid DB path → 503 |
| K-006 | `k8s/pdb.yaml` contains a `PodDisruptionBudget` with `minAvailable >= 1` and correct selector; `maxUnavailable` (if used instead) must be `<= 1` |
| K-007 | No `ClusterRoleBinding` to `cluster-admin` for the SA; a `Role` exists with non-wildcard verbs; a `RoleBinding` connects the correct SA to that Role |
| K-008 | `runAsNonRoot: true`; `allowPrivilegeEscalation: false`; `capabilities.drop` contains `ALL`; `privileged` not true |
| K-009 | `API_KEY` absent from ConfigMap; present in Secret (`data` or `stringData`) |
| T-001 | No `timestamp()` in `main.tf`; `null_resource` still exists |
| T-002 | `backend.tf` does not use `backend "local"`; a recognised remote backend is configured |
| C-001 | `deploy-production` job has `when: manual` |
| M-001 | `HighErrorRate` threshold > 0; `for:` clause present; division operator present outside label selectors |

### K-005 validator subprocess design

Run as a subprocess (fresh Python process each time — no `importlib.reload`). Redirect structlog to stderr so only the HTTP status code goes to stdout:

```python
import os, sys, logging
os.environ["DB_PATH"] = "{db_path}"
logging.disable(logging.CRITICAL)
import structlog
structlog.configure(logger_factory=structlog.PrintLoggerFactory(file=sys.stderr))
sys.path.insert(0, "app")
import app as a
with a.app.test_client() as c:
    r = c.get("/health")
    print(r.status_code)
```

---

## Design Rules — Do Not Violate These

These were learned through testing. They are non-negotiable.

1. **No `# BUG:`, `# BROKEN:`, or `# PLACEHOLDER:` comments in any candidate-facing file** — problem fixtures, app files, YAML manifests, scripts. These turn diagnosis problems into reading exercises. Keep annotated versions in `interviewer/solutions/` only.

2. **Use `imagePullPolicy: IfNotPresent`** everywhere — never `Never`. `Never` signals a minikube/kind lab to experienced candidates.

3. **`backup.sh` must use `sqlite3 "$DB_PATH" ".backup '$BACKUP_FILE'"` not `cp`** — `cp` on a live SQLite file can produce corrupt backups.

4. **Validators are file-based (YAML parsing)** — do not require a running Kubernetes cluster, Docker daemon, or Terraform provider. The lab must work on any macOS laptop without cloud credentials.

5. **No hardcoded laptop paths** — use `REPO_ROOT = Path(__file__).parent.resolve()` computed at runtime.

6. **The baseline (`main` branch) is the working/correct state** — problem fixtures contain only the broken files. When a problem is activated, broken files overwrite the working baseline. Reset restores the working baseline.

7. **`./interview reset` is git-based only** — `git reset --hard HEAD` + `git clean -fdx`. No Docker or Kubernetes cleanup needed.

8. **Commit the fix to git before any test that calls `./interview reset`** — otherwise reset will wipe uncommitted changes.

---

## Scoring Rubric

### Categories and weights

| # | Weight | Category |
|---|---|---|
| 1 | 1× | Linux/shell fundamentals |
| 2 | 1× | Docker |
| 3 | 1× | Kubernetes |
| 4 | 1× | Terraform/IaC |
| 5 | 1× | CI/CD |
| 6 | 1× | Monitoring/observability |
| 7 | **2×** | Troubleshooting & root cause |
| 8 | **2×** | Validation discipline |
| 9 | **2×** | Claude Code usage quality |
| 10 | 1× | Communication |
| 11 | **3× (senior only)** | Judgment: right fix vs. convenient fix |

### Scoring formula

```
score = cat1 + cat2 + cat3 + cat4 + cat5 + cat6
      + 2×cat7 + 2×cat8 + 2×cat9
      + cat10
      + (3×cat11  ← senior only)
```

### Maximum scores and hire thresholds

| Level | Max | Strong hire | Lean hire | Borderline | No hire |
|---|---|---|---|---|---|
| Mid | 65 | ≥ 50 | 40–49 | 30–39 | < 30 |
| Senior | 80 | ≥ 62 | 50–61 | 37–49 | < 37 |

Thresholds are calibrated at 77% / 62% / 46% of max — consistent across both levels.

---

## Interviewer Deliverables (inside `interviewer/`)

### `interviewer/solutions/{ID}.md` — one per problem

Each solution file must include:
- Root cause (1–2 sentences)
- Files to inspect
- Exact fix (with code)
- What the validator checks
- Common wrong fixes (especially Claude traps for Senior problems)
- Follow-up questions
- Rubric signal notes

### `interviewer/rubric.md`

Full scoring rubric with formula, max scores, hire thresholds, and evidence note requirements.

### `interviewer/interviewer-guide.md`

Includes: what to observe, green flags, red flags, when and how to give hints, follow-up question bank, how to distinguish AI-assisted understanding from prompt-engineering, mandatory post-problem question: "Without Claude, how would you approach this?"

---

## `setup.sh` — One-Shot Laptop Setup

An idempotent shell script that sets up a new macOS laptop for running interviews. It must:

1. Check for Homebrew; install if missing
2. Check for Python 3.9+; install `python@3.11` via brew if not met
3. Check for git; install via brew if missing
4. Check for sqlite3; install via brew if missing
5. Check for Claude Code (`claude`); install via `brew install claude` if missing
6. Clone the repo if not already present; skip if already inside the repo
7. `pip3 install pyyaml flask structlog prometheus-client --quiet`
8. `chmod +x interview`
9. Run `./interview reset` + `./interview list` to verify

Must use colour-coded output (✅ green for skip/done, ➜ yellow for installing). Safe to re-run on an already-configured laptop.

Downloadable via:
```bash
curl -fsSL https://raw.githubusercontent.com/{owner}/{repo}/main/setup.sh -o setup.sh
chmod +x setup.sh && ./setup.sh
```

---

## README Requirements

The README must include:
1. What the lab is (2–3 sentences)
2. **"Setting up on a new laptop"** — Option A (run `setup.sh`) and Option B (manual 8-step instructions)
3. Full problem bank table (all 15 problems)
4. Running an interview — start, two-terminal workflow diagram, candidate commands, reset
5. Interview format (60 min total — 10 intro, 12 hands-on, 15 explanation, 15 follow-up, 8 scoring)
6. Scoring — formula, max scores, hire threshold tables for Mid and Senior
7. Repo structure
8. How the runner works
9. Candidate instructions section (no spoilers)

---

## Verification Checklist

After building, verify end-to-end:

```bash
# 1. Setup script syntax
bash -n setup.sh && echo "syntax OK"

# 2. Reset
./interview reset   # exit 0, working tree clean

# 3. List
./interview list
./interview list --level senior

# 4. Start (pipe name to avoid interactive prompt in test)
echo "Test Candidate" | ./interview start --level mid

# 5. Status (shows name, level, elapsed, remaining)
./interview status

# 6. Validate broken state — must fail with specific message
./interview validate

# 7. Fix current problem, validate — must pass with ▶ next prompt
./interview validate

# 8. Advance and complete all 5
./interview next
# ... repeat until all 5 solved

# 9. Final validate — must show personalised congratulations or overtime message
# 10. Next after completion
./interview next   # "You have finished... Run reset to restart."

# 11. Reset — git clean, state file gone
./interview reset
git status         # nothing to commit, working tree clean
```

The lab is ready when all 11 steps pass without error.
