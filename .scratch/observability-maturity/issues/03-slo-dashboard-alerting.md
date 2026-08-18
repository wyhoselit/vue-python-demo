# 03 — SLO-based Observability Dashboard & Alerting

**What to build:** A Grafana dashboard visualizing Availability (99.9%) and Latency (P95 < 200ms) SLIs, with automated Telegram alerts for burn-rate breaches and PagerDuty escalation after 15m unacknowledged.

**Blocked by:** None — can start immediately.

**Status:** ready-for-agent

- [ ] Grafana dashboard displays Availability and P95 Latency as Stat panels
- [ ] Prometheus alert rules trigger on error budget burn rate (1h/6h windows)
- [ ] Alertmanager routes alerts to Telegram bot via webhook
- [ ] Telegram bot escalates to PagerDuty if unacknowledged >15m
- [ ] Test: Inject artificial 5xx errors → alert fires in Telegram → escalates to PagerDuty after 15m