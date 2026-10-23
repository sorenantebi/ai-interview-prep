---
topic: "Search & Analytics"
difficulty: Hard
problem: "Metrics Monitoring"
---
# Design a Metrics Monitoring Platform

**Topic:** Search & Analytics · **Difficulty:** Hard · **Answer:** Metrics Monitoring - Solution

## Prompt

Design a metrics monitoring and alerting platform in the spirit of Datadog or Prometheus plus Grafana. Servers and services emit numeric metrics (CPU, request latency, error counts). Engineers view them on dashboards, run queries over time ranges, and get alerted when something looks wrong.

## Requirements to pin down (ask the interviewer)

- Push or pull collection model, and which metric types (counter, gauge, histogram)?
- Resolution and retention: 10 s data for how long, and rolled-up data for how long?
- How quickly must an alert fire after a problem starts?
- Which query features are needed: label filters, aggregations (sum/avg/p99), group-by?
- Single tenant or multi-tenant? Do we need to protect against noisy tenants?
- Is the monitoring system for internal infrastructure only?

## Scale hints

- ~100K hosts, ~100 metrics per host, reported every 10 seconds (on the order of 1M data points per second)
- Roughly 10M distinct time series (label combinations)
- Dashboards must load in about a second for common ranges
- Monitoring must keep working when the system it monitors is failing

## Think about before opening the answer

1. What does the write path look like for 1M points per second, and which store fits time-series data?
2. How would you compress data points, and why are time series so compressible?
3. How do you keep dashboards fast for "last 30 days" queries without scanning raw data?
4. How does alert evaluation work, and how do you avoid missed or duplicate alerts?
5. What is high cardinality, and why can one bad label take down the system?
6. How do you handle the monitoring system's own failures?

## Self-check

- [ ] I can estimate ingest rate, storage per day and the effect of compression and rollups
- [ ] I can describe a TSDB write path (WAL, head block, immutable blocks, compaction)
- [ ] I can design downsampling and retention tiers
- [ ] I can design alert evaluation, de-duplication and notification routing
