# Interview Scoring Rubric

Score each category 1–5. Use half-points if needed. Categories 7, 8, 9 are weighted **2×**. Category 11 is weighted **3×** for senior candidates only.

---

## Categories

| # | Category | Score 1 — Poor | Score 3 — Acceptable | Score 5 — Strong |
|---|---|---|---|---|
| 1 | Linux/shell fundamentals | Confused by `ls`, `cat`, `grep` | Reads files, uses pipes confidently | Idiomatic: `jq`, `kubectl -o jsonpath`, `awk`, `diff` |
| 2 | Docker | Can't explain image vs container | Reads Dockerfile, runs `docker build` | Reasons about layers, root user, image tags, multi-stage |
| 3 | Kubernetes | Can't find a manifest | Reads probes, services, configmaps correctly | Cross-references selectors, ports, secrets, RBAC |
| 4 | Terraform/IaC | Doesn't recognise `.tf` files | Reads variables, runs `terraform plan` | Reads plan output, understands force-new, backend config |
| 5 | CI/CD | Doesn't know what `.gitlab-ci.yml` does | Edits stages, sees pipeline order | Reasons about approval gates, secrets, deployment safety |
| 6 | Monitoring/observability | Never opens `monitoring/` | Reads PromQL expressions | Tunes thresholds, understands `for:`, debates SLO impact |
| 7 (**2×**) | Troubleshooting & root cause | Guesses and retries blindly | Forms hypothesis, tests it | States root cause clearly; predicts validation outcome before running |
| 8 (**2×**) | Validation discipline | Never runs `./interview validate`, doesn't read output | Runs validate after fixing | Validates incrementally; predicts pass/fail before running |
| 9 (**2×**) | Claude Code usage quality | Pastes full files, accepts everything Claude says | Asks pointed questions, reads suggestions before applying | Rejects wrong suggestions with explanation; cross-checks with file content |
| 10 | Communication | Can't explain what they changed or why | Walks through fix coherently | Root cause → fix → impact → prevention — all clear and concise |
| 11 (**3×, senior only**) | Judgment: right fix vs. convenient fix | Picks Claude's first suggestion without analysis | Considers alternatives, picks the correct one | Catches cases where Claude is wrong; explains why the shortcut is dangerous |

---

## Score Interpretation

| Weighted Total | Recommendation |
|---|---|
| ≥ 40 | **Strong hire** — recommend to next round |
| 30–39 | **Lean hire** — discuss specific gaps |
| 20–29 | **Borderline** — significant gaps in key areas |
| < 20 | **No hire** |

*For senior candidates, add 10 points to the threshold (category 11 at 3× adds up to 15 points to max score).*

---

## Evidence Notes

For each category, the interviewer should write 1–2 sentences of evidence:

> **Category 9 — Claude Code usage:**
> Candidate asked Claude "what does the livenessProbe field do in Kubernetes?" then read the deployment.yaml manually to verify the path before applying the fix. Rejected Claude's suggestion to remove the probe entirely. → **Score 5**

Evidence notes are mandatory before submitting scores.
