---
topic: "Infrastructure & Scheduling"
difficulty: Medium
problem: "Job Scheduler"
---
# Design a Distributed Job Scheduler – Solution

**Topic:** Infrastructure & Scheduling · **Difficulty:** Medium · **Question:** Job Scheduler - Question

## 1. Requirements

**Functional**
- Create a job: one-off (`runAt`), delayed, or recurring (cron expression); payload and target (HTTP callback or task type)
- Cancel / pause / update a job; query status and run history
- Execute jobs on workers with timeouts and automatic retries with backoff

**Non-functional**
- Durable: a created job is never lost
- **At-least-once** execution; users make jobs idempotent (we supply an idempotency key per run)
- Timeliness: start within ~1-2 s of due time at p99
- Scales to ~100M stored jobs and ~10K due/s; no single point of failure
- Fairness: one tenant's burst must not starve others

**Out of scope:** DAG / workflow dependencies (mention as a layer on top), the business logic inside jobs, exactly-once side effects.

## 2. Back-of-envelope

- Job row ≈ 1 KB (payload, schedule, status, retry state). 100M × 1 KB ≈ **100 GB** live, plus history/run records (~200 B per run, TTL 30 days).
- 10K due jobs/s ≈ 860M runs/day, so run records need an append-friendly store or heavy TTL. Typical load is far below peak.
- If a poll returns batches of 500 rows, 10K/s is only ~20 polls/s in total. Polling is cheap **if the due-time index is right**.
- Worker fleet: avg job 2 s, 10K/s peak ≈ 20K concurrent jobs ≈ ~1-2K workers with 10-20 slots each.

## 3. Core entities and API

Entities: `Job { jobId, tenantId, schedule (runAt | cron), payload, target, maxAttempts, timeoutSec, status, nextRunTime, attempt, leaseOwner, leaseExpiry, idempotencyKey }`, `Run { jobId, runId, attempt, startedAt, finishedAt, result }`.

```
POST   /jobs              { schedule, payload, target, maxAttempts?, timeoutSec? } -> { jobId }
GET    /jobs/{id}         -> job + recent runs
DELETE /jobs/{id}         cancel (marks CANCELLED; workers check before running)
POST   /jobs/{id}/pause | /resume
```

## 4. High-level design

!Job Scheduler - Diagram.excalidraw

- The **Job API** validates and writes the job to the **Job Store**, indexed by `(shard, nextRunTime)`.
- The **Scheduler** repeatedly asks for jobs whose `nextRunTime <= now`, atomically marks them as claimed, and pushes `jobId` messages onto a **queue**. It does no execution itself.
- **Workers** pull messages, take a **lease**, run the job against the target, heartbeat while running, and write the result.
- Failures retry with backoff and finally land in a **dead-letter queue**. Cron jobs compute the next `nextRunTime` after each run.
- Scheduler instances coordinate through etcd/ZooKeeper (or the DB itself) so shards of the time space have exactly one active owner.

## 5. Deep dives

### 5.1 Storage and the "due now" query

| Option | Pros | Cons |
|---|---|---|
| **Postgres/MySQL, sharded by `jobId`, index on `(status, nextRunTime)`** | Transactions, `SELECT ... FOR UPDATE SKIP LOCKED`, simple | Needs sharding at 100M+ rows with high write rate |
| DynamoDB / Cassandra, partition = time bucket (e.g. minute + shard no.) | Scales horizontally, cheap range scans per bucket | No cross-row transactions; claim needs conditional writes |
| Redis sorted set (score = runAt) | Very fast `ZRANGEBYSCORE` | Durability and memory cost; fine only as a cache of the next minute |
| Kafka delay topics | Reuses infra | No arbitrary delay, awkward cancellation |

**Recommended:** a sharded relational store, or a KV store partitioned by time bucket plus a **partial index on `status = SCHEDULED`**. To avoid hot partitions at the top of a minute, add a shard suffix: `bucket = (minute, hash(jobId) % N)`.

### 5.2 Claiming jobs without duplicates

Poll loop per scheduler shard, every ~500 ms:

```sql
UPDATE jobs SET status='QUEUED', lease_owner=:me
WHERE job_id IN (SELECT job_id FROM jobs
                 WHERE status='SCHEDULED' AND next_run_time <= now()
                 AND shard = :s ORDER BY next_run_time LIMIT 500
                 FOR UPDATE SKIP LOCKED)
RETURNING job_id;
```

- `SKIP LOCKED` lets several schedulers poll the same shard without blocking or double-claiming. On KV stores use a conditional write (`status = SCHEDULED` to `QUEUED`).
- Scheduler then enqueues the claimed ids. If it dies after claiming but before enqueuing, a **reaper** resets rows stuck in `QUEUED` for longer than a threshold.
- Pre-fetch: load the next 30-60 s of jobs into memory and sleep until due, giving sub-second precision without hammering the DB.
- Leader election per shard (etcd lease) is the alternative to lock-free claiming. It is simpler to reason about, but failover delay hurts timeliness.

### 5.3 Execution, leases and worker failure

!Job Scheduler - Deep Dive Diagram.excalidraw

- A worker pulling a message sets `status=RUNNING, leaseExpiry = now + 30 s` and **extends the lease by heartbeat** every ~10 s.
- If a worker dies, heartbeats stop, the lease expires and the reaper moves the job back to `SCHEDULED` for another attempt. This gives **at-least-once**: a slow (not dead) worker may finish after the lease was reassigned, so two runs can overlap.
- Mitigation: fencing token (the `attempt` number) on result writes, plus a per-run **idempotency key** passed to the target so the downstream can dedupe.
- Exactly-once is not achievable end to end against an arbitrary external target. Say so, and offer at-least-once + idempotency.
- Queue choice: SQS-style visibility timeout gives leases for free; Kafka needs partition-per-consumer and gives poor per-message retry, so prefer SQS/RabbitMQ-style or a DB-backed queue.

### 5.4 Recurring jobs, retries, backoff

- **Cron:** after each run completes (or is skipped), compute the next occurrence from the *scheduled* time, not the finish time, to avoid drift. Store `nextRunTime` on the same row, in one transaction with the status update. Handle time zones and DST by storing the cron expression plus IANA zone.
- Missed runs (system was down): policy per job: run once now ("catch up") or skip to the next slot.
- **Retries:** `nextRunTime = now + base × 2^attempt + jitter`, capped. After `maxAttempts`, mark DEAD, push to DLQ, alert the owner.
- Per-run timeout enforced by the worker; a job that exceeds it is killed and counts as a failed attempt.

### 5.5 Scale, fairness and the thundering herd

- Many jobs are scheduled at `:00` of each minute or hour. Spread polling across shards, add random start jitter for jobs that allow it, and use bounded worker concurrency per tenant.
- **Priority / fairness:** separate queues per priority tier; per-tenant concurrency caps and weighted round robin so one tenant with 5M jobs does not block the rest.
- **Autoscale** workers on queue depth and age of the oldest due job (the SLO metric: "lag = now − nextRunTime").
- Poison jobs (always crash the worker) hit the retry cap and the DLQ rather than looping forever.

### 5.6 Operations

- Metrics: scheduling lag p99, queue age, retry rate, DLQ size, lease expiries.
- History: write run records to a TTL'd store; keep only the last N runs on the job row.
- Cancel: set `CANCELLED`; workers re-check status immediately before invoking the target.

## 6. What interviewers look for

- **Junior:** jobs table with `nextRunTime`, a poller, workers, basic retry.
- **Mid:** safe claiming of rows, queue between scheduler and workers, leases with heartbeat, cron recomputation, at-least-once reasoning.
- **Senior:** sharding the time index and avoiding hot buckets, fencing tokens and idempotency keys, scheduler failover, fairness across tenants, lag SLO and autoscaling, honest take on exactly-once.

## 7. Common pitfalls

- Promising exactly-once execution
- A single scheduler process (SPOF) or many pollers without a claim protocol
- Scanning the whole table instead of using an index on due time
- No lease/heartbeat, so a dead worker's job is lost forever
- Retrying instantly with no backoff or cap, hammering a failing target
- Computing the next cron time from "now" and drifting
