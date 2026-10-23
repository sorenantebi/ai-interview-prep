---
topic: "Infrastructure & Scheduling"
difficulty: Medium
problem: "LeetCode"
---
# Design LeetCode (Online Coding Judge) – Solution

**Topic:** Infrastructure & Scheduling · **Difficulty:** Medium · **Question:** LeetCode - Question

## 1. Requirements

**Functional**
- View a paginated list of problems (title, difficulty, tags)
- View a problem (statement, language-specific starter code/stub)
- Submit code in a chosen language, run it against the test cases, and get a verdict (plus runtime/memory) back quickly
- View a **live leaderboard** for a coding competition (ranked by problems solved and completion time)
- Extensions: own submission history, contest registration/scoring rules

**Non-functional**
- **Availability over consistency** (a slightly stale problem page or leaderboard is fine)
- **Isolation and security first:** user code is untrusted and may try to escape, fork-bomb, read other tests or call the network
- Result returned within **~5 s**; fair, deterministic judging (same code, same verdict)
- Scale to **~100K concurrent competition participants**, with spikes; no submission lost; verdicts are final

**Out of scope:** user authentication, profiles, payments, analytics, social features, forums, editorials, plagiarism detection.

## 2. Back-of-envelope

- ~4,000 problems, each with ~100 test cases; hundreds of thousands of users overall. ~5M submissions/day on a normal day ≈ 60/s average.
- Contest peak: 100K participants; HI-style estimate of **~10K submissions in the same short burst** (a problem opens or a deadline nears), ~1-2K/s sustained over the first minutes. The queue absorbs the burst.
- Judge time per submission: ~2 s wall time including container start. At ~1-2K/s sustained that is ~2-4K concurrent sandboxes; with 8-16 per host (one per core) ≈ **250-500 judge hosts** at contest peak (fewer if verdicts may queue for a few seconds). Autoscaled, mostly idle off-contest.
- Storage: submission ≈ 5 KB source + metadata, 5M/day × 5 KB = 25 GB/day ≈ 9 TB/yr, fine for a partitioned Postgres or a NoSQL store (DynamoDB), cold data in S3.
- Test data: 4K problems × ~10-50 MB ≈ 40-200 GB in S3. Judges cache it locally.
- Result polling: 100K participants polling every ~1 s is ~100K reads/s on the status cache, so results are cached (Redis), not read from the DB.

## 3. Core entities and API

Entities: `Problem { id, slug, statement, stubs{language -> code}, limits {timeMs, memMB}, testSetVersion }` (test cases and expected outputs stored separately), `Submission { id, userId, problemId, competitionId?, language, code, status, verdict, runtimeMs, memKB, createdAt }`, `Leaderboard { competitionId, userId, problemsSolved, penalty/finishTime }` (competition = `Contest { id, start, end, problemIds }`).

```
GET  /problems?page=1&limit=100                 -> problem list
GET  /problems/{id}?language=python             -> statement + language stub
POST /problems/{id}/submit  { language, code }  -> 202 { submissionId }   (job id)
GET  /check/{submissionId}                      -> { status: QUEUED|RUNNING|DONE, verdict?, runtimeMs? }
GET  /leaderboard/{competitionId}?page=1&limit=100  -> ranked users
```

## 4. High-level design

!LeetCode - Diagram.excalidraw

- **Browse path:** Problem Service reads from the problem DB (NoSQL such as DynamoDB, or Postgres; a key-value fit since problems are read by id) with a Redis/CDN cache in front. Statements are read-mostly and cache extremely well.
- **Submit path:** the API/Submission Service validates (size limit, language, rate limit per user), stores the submission with `QUEUED`, publishes a message to the **judge queue** (SQS/Kafka) and immediately returns `202` with the submission (job) ID.
- **Judge workers** are language-specific containers (e.g. Docker on ECS/Kubernetes) that pull a job, fetch the test cases (cached from S3), compile and run in a sandbox, compare outputs, and write the verdict to the **submissions DB and a Redis status cache** at the same time.
- The client **polls** `GET /check/{id}` (or listens on SSE/WebSocket), served from the cache. Polling every ~1 s is simple and enough.
- On an Accepted verdict during a contest, the Contest Service updates the **Redis sorted-set leaderboard**.

## 5. Deep dives

### 5.1 Scaling to 100K participants: why a queue, not inline execution

- *Bad:* run code inside the web request, or scale one big machine vertically. It ties up connections, retries are impossible when a runner dies, and a spike takes the web tier down, with a hard hardware ceiling.
- *Great (A):* scale the API and the container fleet **horizontally** with auto-scaling on CPU/memory.
- *Great (B, recommended for contests):* horizontal scaling **plus a queue** (SQS/Kafka) between the API and the judges. The API stays fast, a spike becomes queueing delay instead of failures, failed jobs are retried, no submission is lost, and workers autoscale on queue depth and age. It adds some moving parts, but resilience is worth it.

Prefer **SQS-style visibility timeouts** (or per-message acks) so a crashed judge's job reappears automatically. Use separate queues, or priorities, for contest vs practice, and for "Run" (samples) vs "Submit".

### 5.2 Running untrusted code safely

- *Bad:* run the code on the API server itself. One malicious or buggy submission can compromise or crash the whole service.
- *Good:* a **virtual machine** per run. Strong isolation but heavy and slow to start.
- *Great (recommended):* **hardened containers** (Docker): lightweight, fast, with read-only filesystem, CPU/memory limits, an explicit timeout (~5 s), no network, and a seccomp syscall allow-list. For stronger isolation against kernel escapes (Staff+ discussion), run the container on a user-space kernel or microVM (gVisor, Firecracker).

Defence in depth, since any one layer can fail:

| Layer | Mechanism |
|---|---|
| Isolation | Per-run container; add a **user-space kernel or microVM** (gVisor, Firecracker) if you want protection from shared-kernel escapes beyond plain Docker |
| Syscalls | seccomp allow-list; no `ptrace`, `mount`, raw sockets |
| Network | None (no network namespace interfaces) |
| Filesystem | Read-only root, tiny writable tmpfs, tests mounted outside the sandbox or fed via stdin |
| Resources | cgroups: CPU time, memory cap, **pids limit** (fork bombs), output size cap |
| Time | Wall-clock timeout plus CPU-time limit (to catch sleep and busy loops) |
| Identity | Unprivileged user, fresh sandbox per submission, destroyed afterwards |

Judge hosts sit in a separate network zone with no credentials and no route to the databases; results go back via the queue / a narrow API. Pre-warmed pools of sandboxes per language hide cold start (~100-300 ms vs seconds).

### 5.3 Judging correctness and fairness

- Run test cases in order of increasing size and **stop at the first failure**, except in contest scoring modes that need partial credit.
- Compare outputs with a per-problem checker: exact match, whitespace-tolerant, floating-point epsilon, or a custom checker program for problems with many valid answers.
- Timing fairness: pin to a dedicated CPU core, disable noisy neighbours (no co-scheduled sandboxes on the same core), allow a language multiplier for slow runtimes, and rerun a borderline TLE once before declaring it.
- Verdict set: Accepted, Wrong Answer, TLE, MLE, Runtime Error, Compile Error, Output Limit, Internal Error (never shown as the user's fault, and automatically retried).
- Judging is **idempotent**: a message may be delivered twice; the result write is conditional on `status != DONE` so the first verdict wins.

### 5.4 Test case storage and delivery

- Test inputs and expected outputs are large, immutable and secret. Store them in **S3, versioned** (`problemId/testSetVersion/`), never in the sandbox image.
- Judge hosts keep an on-disk LRU cache keyed by version; first use pulls from S3. Pre-pull for contest problems before the contest begins.
- **Test case format:** define each test case once, language-independently, using a standard serialization per data structure (e.g. arrays as JSON lists, trees in level-order). Each language's container has a small harness with deserializers that turn the input into native objects, calls the user's function, and serializes the result for comparison. One test definition then serves every language.
- Hidden test inputs are never sent to the browser; on a failure only show the first failing case for public ones, to stop users from reconstructing the test set.

### 5.5 Contests and leaderboard

- *Bad:* query the database (`ORDER BY` + aggregation) on every poll. Overwhelming load at 100K viewers.
- *Good:* periodically refresh a cached leaderboard. Fewer queries, but results can be ~30 s stale.
- *Great (recommended):* a **Redis sorted set** per competition, updated on each accepted submission, with clients polling every ~5 s; lookups (`ZREVRANGE`) are instant and the DB is barely touched.
- Score: points per solved problem + penalty (minutes since start + 5/20 per wrong attempt). Encode as one sortable number, e.g. `score × 10^9 − penaltySeconds`, so rank is a single ZSET score.
- Redis **sorted set** per contest: `ZADD contest:{id}:lb score userId` on each first Accepted per problem; `ZREVRANGE` for the top page, `ZREVRANK` for "your rank". O(log N) with 50K members is trivial.
- Serve the leaderboard from a **cached snapshot** refreshed every 1-2 s (not recomputed per viewer); 50K viewers hitting the same page are served by the CDN or a read cache.
- Source of truth is the submissions DB. If Redis is lost, rebuild the ZSET by replaying accepted submissions of the contest.
- Freezing the board in the last hour is just "stop refreshing the public snapshot".
- Contest start spike: everyone fetches the problem at T0. Pre-warm caches and put statements behind the CDN with a start-time gate enforced by token / signed URL.

### 5.6 Scaling and failure modes

- Autoscale judges on `queue age`; a warm minimum pool before each contest.
- Judge crash: visibility timeout expires, the job is retried (cap at 3, then `Internal Error` plus alert).
- Poison submissions (crash the host sandbox repeatedly) are quarantined to the DLQ for review.
- Per-user rate limit (e.g. 1 submit per 5 s, N per hour) against abuse and queue flooding.
- Multi-region: problem reads from the nearest region; judging pools can sit anywhere because they only pull from the queue.

## 6. What interviewers look for

- **Mid-level:** clear API and data model; a functional high-level design covering problems, submit, execution and leaderboard; understands the container vs VM vs serverless trade-offs for running code; surface-level familiarity with the components (queue, workers, Redis).
- **Senior:** detailed discussion of code execution approaches and isolation, clear trade-offs, proactive problem finding (contest spikes, leaderboard load), test harness and serialization details, deterministic and idempotent judging.
- **Staff+:** drives the whole conversation, anticipates design issues, justifies every decision with trade-offs, and keeps the system simple and scalable without over-engineering; layered isolation (microVM, seccomp, cgroups), contest-spike capacity maths, rebuildable leaderboard, queue prioritisation, operational failure handling.

## 7. Common pitfalls

- Running user code in the API process or without a sandbox
- Containers without limits (no pids / memory / output / network restrictions), or plain Docker as the only isolation for a hostile threat model
- Synchronous execution inside the HTTP request
- Recomputing the leaderboard with SQL `ORDER BY` on every poll
- Shipping hidden test data to the browser, or into a long-lived judge image
- Counting an internal infrastructure error as a user's Wrong Answer
