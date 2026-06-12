# Interviewer Guide — CloudOps Interview Lab

## Setup (Before Candidate Arrives)

1. `cd /path/to/cloudops-interview-lab`
2. `./interview reset` — verify exit 0, clean output
3. `./interview status` — should say "No active interview session"
4. Open VS Code with this repo in the workspace
5. Confirm Claude Code is open in the sidebar panel
6. Confirm `python3`, `docker`, `git`, `kubectl` are in PATH
7. Brief candidate orientation (2 min): explain the lab, show Claude Code is available, run `./interview start --level mid` so they see the format

---

## During the Interview

**Your role:** Silent observer. Take notes on behaviour, not just outcomes.

**What to observe:**

| Behaviour | What it signals |
|---|---|
| Opens the file mentioned in the problem before asking Claude anything | Good DevOps instinct — reads before guessing |
| Asks Claude "what does X field do in K8s?" then verifies in the file | Good AI usage — treats Claude as reference, not oracle |
| Runs `./interview validate` immediately after applying a Claude diff | Validation discipline |
| Reads the validation failure message carefully and adjusts | Diagnostic thinking |
| Accepts Claude's first suggestion for K-005 (add /healthz to app) | Red flag — Claude trap problem |
| Can explain what changed and why when asked | Engineering understanding, not prompt engineering |
| Asks Claude "fix this" without any context | Poor AI usage |
| Changes files without running validate | Poor validation discipline |

---

## Hints

You may give ONE hint per problem if the candidate is clearly stuck for more than 2 minutes and making no progress.

**Hint cost:** deduct 1 point from category 7 (troubleshooting) for the problem where a hint was used.

**How to give a hint without giving away the solution:**

| Problem | Hint to give |
|---|---|
| D-001 | "Look at the FROM line and check if there's a USER directive" |
| D-002 | "What's the difference between ENV and ARG in a multi-stage Dockerfile?" |
| K-001 | "Run `kubectl describe pod <name>` and look at the Events section" |
| K-002 | "How does a Service find which pods to route to?" |
| K-003 | "What happens to a pod that has no resource limits under high load?" |
| K-004 | "Trace the request path: Ingress → Service → Pod. Which port is used at each hop?" |
| K-005 | "What should a readiness probe actually verify about the service?" |
| K-006 | "A rolling update strategy controls deployments. What controls pod eviction during node maintenance?" |
| K-007 | "What level of access does the application actually need?" |
| K-008 | "Look at both the pod-level and container-level securityContext" |
| K-009 | "What is the difference between a ConfigMap and a Secret in Kubernetes?" |
| T-001 | "Run `terraform plan` and look at what it plans to do every time" |
| T-002 | "Where is the Terraform state currently being stored?" |
| C-001 | "What happens to the production deploy job when a merge to main succeeds?" |
| M-001 | "How many errors does it take to trigger this alert?" |

---

## Green Flags

- Uses `git diff` to review their own changes before validating
- Explains root cause before touching any file
- Uses Claude to *understand* a concept, not to *write* the fix
- When Claude is wrong: "Claude suggested X but that's not right because..."
- Validates, sees failure, reads the failure message, adjusts without re-asking Claude
- For senior problems: identifies the secondary risk even after fixing the primary one

## Red Flags

- Can't explain root cause after solving the problem
- Applies a Claude diff without reading it line by line
- Asks Claude "fix all the problems in this file" (too broad)
- Never opens the file being modified
- Removes a probe, a stage, or a resource entirely to "fix" it
- Solves K-005 by adding `/healthz` instead of fixing `/health`
- Solves K-006 by raising `maxSurge` instead of adding a PDB
- Solves K-007 by replacing `cluster-admin` with a Role that has `verbs: ["*"]`

---

## Follow-Up Discussion Questions

Ask these after the hands-on phase. Pick 3–5 based on which problems were solved.

**Root cause & understanding:**
- "Walk me through what was broken and why it caused that specific symptom."
- "What would the production impact have been if this wasn't caught?"

**Validation & operations:**
- "How would you validate this in a real production cluster (not a lab)?"
- "What monitoring or alerting would you add to detect this issue earlier?"
- "What's your rollback plan if this fix causes a regression?"

**Claude Code usage:**
- "What did Claude suggest for this problem?"
- "Was there anything Claude suggested that you didn't use? Why?"
- "Did Claude ever give you wrong or misleading information? How did you spot it?"

**Prevention:**
- "How would you prevent this class of problem from reaching production?"
- "Would this be caught in your current CI pipeline? What would you add?"

**Senior-specific:**
- "For K-007 — what's the minimum viable RBAC policy for this service?"
- "For K-005 — why is a cargo-cult health check dangerous in Kubernetes specifically?"
- "For T-002 — what's the correct sequence to migrate from local to remote Terraform state?"

---

## Evaluating AI-Assisted vs. Human-Understood Answers

After the candidate walks through a fix, ask: "Without Claude, how would you approach this problem?"

If they can answer confidently → their understanding is genuine.
If they can't explain it without Claude → they followed a recipe.

**This question is mandatory for every problem solved.**

---

## After the Interview

1. Score all categories using `interviewer/rubric.md`
2. Write 1–2 sentences of evidence per category
3. Run `./interview reset` to prepare for the next candidate
4. Do NOT leave your notes in the repo — export them to your interview tracking system
