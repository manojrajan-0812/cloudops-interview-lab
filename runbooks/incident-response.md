# Incident Response Runbook — interview-api

## Severity Levels

| Level | Definition | Response Time |
|---|---|---|
| P1 | Complete service outage — all requests failing | 15 min |
| P2 | Partial outage — subset of users affected or degraded performance | 30 min |
| P3 | Non-critical issue — logging, monitoring, or internal tooling | 4 hours |

---

## 1. Pod CrashLoopBackOff

**Symptoms:** Pods restart repeatedly; `kubectl get pods` shows `CrashLoopBackOff`

**Diagnosis:**
```bash
kubectl describe pod <pod-name> -n default
kubectl logs <pod-name> -n default --previous
kubectl get events -n default --sort-by='.lastTimestamp'
```

**Common causes:**
- Liveness probe firing before app finishes starting (check `initialDelaySeconds`)
- Missing environment variable or config
- Application startup error (check logs)

**Resolution:**
- If probe issue: increase `initialDelaySeconds` and `failureThreshold`
- If config issue: check ConfigMap and Secret references match deployment spec
- Rollback: `kubectl rollout undo deployment/interview-api`

---

## 2. Service Returning 502/503

**Symptoms:** Requests return 502 Bad Gateway or 503 Service Unavailable

**Diagnosis:**
```bash
kubectl get endpoints interview-api-svc -n default
kubectl describe service interview-api-svc -n default
kubectl get pods -l app=interview-api -n default
```

**Common causes:**
- Service selector does not match pod labels (endpoints list is empty)
- All pods failing readiness checks
- Ingress backend port mismatch

**Resolution:**
- Check: `kubectl get endpoints` — if no endpoints, fix service selector
- Check: `kubectl describe pod` — if readiness failing, fix /health endpoint or probe
- Check: `kubectl describe ingress` — verify backend service port

---

## 3. OOMKilled Pods

**Symptoms:** Pods are killed with `OOMKilled` exit code

**Diagnosis:**
```bash
kubectl describe pod <pod-name> | grep -A5 "Last State"
kubectl top pods -n default
```

**Resolution:**
- Short-term: increase `resources.limits.memory`
- Long-term: profile the application to understand actual usage
- Rollback if new limits cause throttling: `kubectl rollout undo deployment/interview-api`

---

## 4. Monitoring Alert: HighErrorRate

**Symptoms:** Prometheus fires `HighErrorRate` alert

**Diagnosis:**
```bash
kubectl logs -l app=interview-api -n default --tail=100 | grep -i error
kubectl exec -it <pod> -- curl http://localhost:8080/health
```

**Common causes:**
- Database connectivity issue (check /health returns 503)
- Application bug in a recently deployed version
- Dependency unavailable

**Resolution:**
- If DB issue: check DB connectivity, alert DB team
- If recent deploy: `kubectl rollout undo deployment/interview-api`
- If persistent: escalate to P2/P1

---

## Contacts

| Role | Contact |
|---|---|
| On-call engineer | PagerDuty rotation |
| Database team | #db-oncall Slack |
| Platform/k8s | #platform Slack |
