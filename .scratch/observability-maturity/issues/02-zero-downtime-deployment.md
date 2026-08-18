# 02 — Hardened Zero-Downtime Deployment Strategy

**What to build:** Kubernetes rolling updates that maintain 100% service capacity at all times (`maxUnavailable: 0`) with controlled `maxSurge`.

**Blocked by:** 01 — Deep Readiness Probe (ensures new pods are healthy before old ones are terminated).

**Status:** ready-for-agent

- [ ] Deployment spec sets `strategy.type: RollingUpdate`
- [ ] `rollingUpdate.maxUnavailable: 0`
- [ ] `rollingUpdate.maxSurge: 25%`
- [ ] Test: Deploy new version → no downtime observed under load
- [ ] Test: New pods are Ready before old pods are terminated