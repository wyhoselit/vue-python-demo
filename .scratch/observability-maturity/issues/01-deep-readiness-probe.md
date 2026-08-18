# 01 — Deep Readiness Probe for Backend Stability

**What to build:** The Ingress will only route traffic to backend pods that have verified their database connectivity, preventing 500 errors during pod startup or transient DB flakiness.

**Blocked by:** None — can start immediately.

**Status:** ready-for-agent

- [ ] Backend health endpoint checks PostgreSQL connection
- [ ] Kubernetes readiness probe calls the health endpoint
- [ ] Pod does not enter "Ready" state until DB connection is confirmed
- [ ] Traffic is blocked from unready pods by Ingress
- [ ] Test: Simulate DB failure → pod becomes NotReady → no traffic flows