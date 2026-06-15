# Interview Scoring Rubric

Score each category 1–5. Half-points are allowed.

---

## Categories

| # | Weight | Category | Score 1 — Poor | Score 3 — Acceptable | Score 5 — Strong |
|---|---|---|---|---|---|
| 1 | 1× | Linux/shell fundamentals | Confused by `ls`, `cat`, `grep` | Reads files, uses pipes confidently | Idiomatic: `jq`, `kubectl -o jsonpath`, `awk`, `diff` |
| 2 | 1× | Docker | Can't explain image vs container | Reads Dockerfile, runs `docker build` | Reasons about layers, root user, image tags, multi-stage |
| 3 | 1× | Kubernetes | Can't find a manifest | Reads probes, services, configmaps correctly | Cross-references selectors, ports, secrets, RBAC |
| 4 | 1× | Terraform/IaC | Doesn't recognise `.tf` files | Reads variables, runs `terraform plan` | Reads plan output, understands force-new, backend config |
| 5 | 1× | CI/CD | Doesn't know what `.gitlab-ci.yml` does | Edits stages, sees pipeline order | Reasons about approval gates, secrets, deployment safety |
| 6 | 1× | Monitoring/observability | Never opens `monitoring/` | Reads PromQL expressions | Tunes thresholds, understands `for:`, debates SLO impact |
| 7 | **2×** | Troubleshooting & root cause | Guesses and retries blindly | Forms hypothesis, tests it | States root cause clearly; predicts validation outcome before running |
| 8 | **2×** | Validation discipline | Never runs `./interview validate`, doesn't read output | Runs validate after fixing | Validates incrementally; predicts pass/fail before running |
| 9 | **2×** | Claude Code usage quality | Pastes full files, accepts everything Claude says | Asks pointed questions, reads suggestions before applying | Rejects wrong suggestions with explanation; cross-checks with file content |
| 10 | 1× | Communication | Can't explain what they changed or why | Walks through fix coherently | Root cause → fix → impact → prevention — all clear and concise |
| 11 | **3× (senior only)** | Judgment: right fix vs. convenient fix | Picks Claude's first suggestion without analysis | Considers alternatives, picks the correct one | Catches cases where Claude is wrong; explains why the shortcut is dangerous |

---

## Scoring Formula

```
score = cat1 + cat2 + cat3 + cat4 + cat5 + cat6
      + 2×cat7 + 2×cat8 + 2×cat9
      + cat10
      + (3×cat11  ← senior only; omit for mid)
```

**Maximum possible scores:**

| Level | Formula | Max |
|---|---|---|
| Mid | Σ(cat1–10) with 2× on 7,8,9 | **65** |
| Senior | Same + 3×cat11 | **80** |

---

## Hire Thresholds

### Mid (max 65)

| Score | Recommendation |
|---|---|
| ≥ 50 | **Strong hire** — recommend to next round |
| 40–49 | **Lean hire** — discuss specific gaps with hiring manager |
| 30–39 | **Borderline** — significant gaps; pass unless exceptional in one area |
| < 30 | **No hire** |

### Senior (max 80)

| Score | Recommendation |
|---|---|
| ≥ 64 | **Strong hire** — recommend to next round |
| 52–63 | **Lean hire** — discuss specific gaps with hiring manager |
| 40–51 | **Borderline** — significant gaps; pass unless exceptional in one area |
| < 40 | **No hire** |

*Thresholds are set at 77%, 62%, and 46% of max respectively — consistent across both levels.*

---

## Evidence Notes

For each category, write 1–2 sentences of evidence before submitting scores. Do not score from memory.

> **Category 9 — Claude Code usage:**
> Candidate asked Claude "what does the livenessProbe field do in Kubernetes?" then read the deployment.yaml manually to verify before applying. Rejected Claude's suggestion to remove the probe entirely and explained why. → **Score 5**

Evidence notes are mandatory.
