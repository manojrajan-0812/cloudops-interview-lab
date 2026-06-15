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

## Setting Up on a New Laptop

Follow these steps in order on a fresh macOS machine.

### Step 1 — Install system dependencies

**Python 3.9+**
```bash
python3 --version
# If missing or < 3.9, install via Homebrew:
brew install python@3.11
```

**Git**
```bash
git --version
# If missing:
brew install git
```

**SQLite3** (used by the backup script)
```bash
sqlite3 --version
# Already installed on macOS by default.
# If missing: brew install sqlite
```

### Step 2 — Install Claude Code (recommended AI assistant)

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

> If `npm` is not available: `brew install node`
>
> Claude Code requires an Anthropic account. Sign in with `claude` after installation.
> Candidates can still use browser-based AI (ChatGPT, Gemini) if Claude Code is not set up.

### Step 3 — Clone the repository

```bash
git clone https://github.com/manojrajan-0812/cloudops-interview-lab.git
cd cloudops-interview-lab
```

### Step 4 — Install Python dependencies

```bash
pip3 install pyyaml flask structlog prometheus-client
```

### Step 5 — Make the runner executable

```bash
chmod +x interview
```

### Step 6 — Verify the setup

```bash
./interview reset
```

Expected output:
```
✅ Interview environment reset successfully.
   Working tree restored to clean baseline.
   Ready for next candidate.
```

```bash
./interview list
```

Expected output: all 15 problems listed with IDs, levels, and titles.

### Step 7 — Run a dry-run before the first candidate

```bash
echo "Test Candidate" | ./interview start --level mid
./interview status
./interview reset
```

If all three commands complete without errors, the laptop is ready.

---

## AI Assistant Options

Candidates can use either of the following during the interview:

**Option 1 — Claude (recommended):** Open a new terminal tab and run:
```bash
cd /path/to/cloudops-interview-lab
claude
```

**Option 2 — Any browser-based AI:** Open [ChatGPT](https://chatgpt.com) or [Gemini](https://gemini.google.com) in a browser.

---

## Running an Interview

### Interviewer: start the session

```bash
./interview start --level mid      # for Mid-level candidates
./interview start --level senior   # for Senior candidates
```

The runner will prompt for the candidate's name, then show a welcome message, the 12-minute time limit, and the first problem.

```
Enter your name: Sarah Johnson

============================================================
  All the best, Sarah Johnson!
  You have 12 minutes to complete the task.
  ...
============================================================
```

To preview the full problem bank before starting:

```bash
./interview list                   # show all 15 problems
./interview list --level senior    # filter by level
```

### Two-terminal workflow

The recommended setup uses two terminal windows side by side:

| Terminal | Purpose |
|---|---|
| **Terminal 1** — Interview | `./interview start`, `./interview validate`, `./interview next` |
| **Terminal 2** — Work | Claude (`claude`), your editor, or a browser AI — fix files here |

```
Terminal 1 (interview)             Terminal 2 (work)
──────────────────────             ─────────────────────────────
./interview start --level mid      # open Claude or browser AI
  → problem appears                # read the broken file
                                   # implement the fix
./interview validate
  → ✅ pass or ❌ hint             # adjust fix if needed
./interview next
  → next problem                   # move to the next broken file
```

### Candidate: investigate → fix → validate → repeat

```bash
./interview validate     # check if the current fix is correct
./interview next         # move to the next problem (after validating)
./interview status       # show progress, elapsed time, and remaining time
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

11 categories scored 1–5. Key categories are weighted:

- **Troubleshooting & root cause** — 2×
- **Validation discipline** — 2×
- **Claude Code usage quality** — 2×
- **Judgment: right fix vs. convenient fix** — 3× (senior only)

**Formula:** `Σ(cat1–6) + 2×cat7 + 2×cat8 + 2×cat9 + cat10 + (3×cat11 senior only)`

| Level | Max score | Strong hire | Lean hire | Borderline |
|---|---|---|---|---|
| Mid | 65 | ≥ 50 | 40–49 | 30–39 |
| Senior | 80 | ≥ 62 | 50–61 | 37–49 |

See `interviewer/rubric.md` for the full rubric, `interviewer/interviewer-guide.md` for observation tips and follow-up questions, and `interviewer/solutions/` for per-problem solution guides.

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

> **If you are a candidate:** the interviewer will run `./interview start`. You will be prompted for your name, then your first problem appears. You have 12 minutes to complete 5 problems.
>
> **To use Claude:** open a new terminal tab, `cd` to this directory, and type `claude`.
> **To use another AI:** open ChatGPT or Gemini in a browser.
>
> Read files yourself before applying any AI suggestion. Always run `./interview validate` after making a fix.
>
> **Do not open the `interviewer/` folder.**

---

## License

MIT
