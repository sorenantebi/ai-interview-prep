---
topic: "Fintech"
difficulty: Hard
problem: "Payment System"
---
# Design a Payment System – Solution

**Topic:** Fintech · **Difficulty:** Hard · **Question:** Payment System - Question

## 1. Requirements

**Functional**
- Merchants create a payment (amount, currency, payment method token) and get a result
- Support authorize, capture, void and refund; query payment status
- Notify merchants of final outcomes (webhooks); expose a ledger/balance and settlement reports

**Non-functional**
- **Exactly-once effect:** no double charge, no lost payment, even with retries and crashes
- Strong consistency for money state; full audit trail; durability (no acknowledged payment lost)
- Availability ~99.99% on payment creation; tolerate slow or failing PSPs
- Security/compliance: PCI DSS, encryption, tokenization, fraud checks

**Out of scope:** building a card network connection, chargeback workflow details, tax.

## 2. Back-of-envelope

- 1M payments/day ≈ 12 TPS average; peak 10x ≈ **~100-1,000 TPS**. This is small for a database: Postgres handles it; the difficulty is **correctness**, not throughput.
- Each payment: ~1 KB payment record + ~4-6 ledger entries × 200 B ≈ 2 KB ⇒ 2 GB/day ≈ **~730 GB/year**, retained for 7+ years for audit. Partition by time.
- PSP latency 1-3 s ⇒ at 1,000 TPS ≈ 3,000 in-flight calls. Use async I/O and per-PSP concurrency limits, never a DB transaction open across the call.

## 3. Core entities and API

Entities: `Payment { id, merchantId, amount, currency, status, pspRef, idempotencyKey, createdAt }`, `PaymentAttempt { id, paymentId, psp, status, rawResponse }`, `LedgerEntry { id, txId, account, direction: DEBIT|CREDIT, amount, currency, createdAt }`, `Account { id, owner, type }`, `IdempotencyRecord { merchantId, key, requestHash, responseBody }`.

```
POST /v1/payments   Idempotency-Key: <uuid>   { amount, currency, paymentMethodToken, captureNow }
                                           -> 201 { id, status: PENDING|AUTHORIZED|SUCCEEDED|FAILED }
GET  /v1/payments/{id}
POST /v1/payments/{id}/capture | /refund
POST webhook to merchant:  payment.succeeded / payment.failed  (signed, retried)
```

## 4. High-level design

!Payment System - Diagram.excalidraw

- The **gateway** authenticates the merchant and checks the idempotency key. The **Payment Service** owns the payment state machine in Postgres.
- It calls the **PSP / card network** to authorize or capture, and records the result. State changes plus an **outbox** row are written in one transaction; a relay publishes the events to **Kafka**.
- The **Ledger Service** consumes events and posts balanced double-entry records. The **Webhook Dispatcher** notifies merchants with retries. A **Reconciliation Worker** compares our books with the PSP's settlement files.
- Card data never enters the core: the checkout form posts to a **tokenization vault** (PCI scope isolated) and the core only sees tokens.

## 5. Deep dives

### 5.1 Idempotency (never charge twice)

- The merchant sends `Idempotency-Key` per logical payment. A table `idempotency(merchantId, key) UNIQUE` stores `requestHash`, status and the final response.
- Flow: insert the key row (unique constraint serializes concurrent duplicates) → if it already exists, return the stored response (or 409 if still in progress, or 422 if `requestHash` differs) → else process and store the response.
- The same key is propagated to the PSP (most PSPs support idempotency keys or merchant reference), so a retry from us to the PSP is also safe.

### 5.2 State machine and ambiguous outcomes

`CREATED → PENDING (sent to PSP) → AUTHORIZED → CAPTURED/SUCCEEDED`, with exits `FAILED`, `VOIDED`, `REFUNDED`. Only legal transitions are allowed, enforced by `UPDATE ... WHERE status = :expected` (optimistic concurrency).

!Payment System - Deep Dive Diagram.excalidraw

- **Timeout from the PSP = unknown, not failed.** Mark the payment `PENDING`, never retry blindly with a new reference. Resolve by (a) retrying the same idempotent call, (b) querying PSP by our reference, (c) waiting for the async webhook, (d) reconciliation.
- Persist intent **before** calling the PSP (write `PENDING` + attempt row, commit), call the PSP **outside** any transaction, then persist the outcome. If we crash in between, a recovery job scans stale `PENDING` rows and queries the PSP.
- PSP webhooks are untrusted input: verify signature, dedupe by event id, and apply them as state transitions.
- Multiple PSPs: route by cost/success rate; fail over only when the first call is *known* not to have charged.

### 5.3 Double-entry ledger

- Every money movement is a transaction with balanced entries (sum of debits = sum of credits), e.g. customer charge 100: debit `PSP_receivable` 100, credit `merchant_pending` 97, credit `fees_revenue` 3.
- **Append-only, immutable:** corrections are new reversing entries; balances are derived (or cached with periodic verification). Gives auditability and detects bugs (the books must always balance).
- Store in Postgres with a unique `(txId, entryIndex)`; consumers are idempotent by `txId`. Partition by time; hot merchant accounts can be contention points, so use sub-accounts or batch postings.
- Why not just a `balance` column? Updates lose history, make retries dangerous and cannot be audited.

### 5.4 Reliable events: outbox and webhooks

- **Dual-write problem:** updating Postgres and publishing to Kafka are not atomic. Use the **transactional outbox**: write the event in the same transaction as the state change; a relay (CDC/Debezium or poller) publishes it at least once. Consumers dedupe by event id.
- Webhooks: at-least-once with exponential backoff (minutes to 3 days), HMAC signature, an event id for merchant-side dedup, and a replay API. Merchants should still be able to `GET` the status.

### 5.5 Reconciliation (the final safety net)

- Daily (and intra-day) compare our ledger with the PSP/bank settlement files: match by PSP reference and amount. Classify mismatches: missing on our side (PSP charged, we show failed), missing on theirs, amount differences, and open them as tickets or automated fixes (refund, re-post).
- This catches everything that retries, timeouts and bugs miss; interviewers expect it to be mentioned.

### 5.6 Scale, consistency and security

- Postgres is the source of truth for payments, partitioned/sharded by `merchantId` if needed; synchronous replica for durability; PITR backups. Use serializable or row-level conditional updates on money state; avoid eventual consistency here.
- Kafka for async side effects only (ledger, webhooks, analytics), **not** for deciding payment correctness.
- Fraud scoring (rules plus ML) runs before authorization with a strict latency budget (~50-100 ms) and a fail-open/closed policy per merchant risk.
- Security: TLS everywhere, secrets in a KMS/HSM, field-level encryption, PCI scope limited to the vault, audit logs, per-merchant API keys with rate limits.

## 6. What interviewers look for

- **Junior:** API, a payment table, calling a PSP, basic status handling.
- **Mid:** idempotency keys, state machine, async webhooks, retries and a message queue.
- **Senior:** handling PSP timeouts as unknown state, write-ahead intent, outbox pattern, double-entry append-only ledger, reconciliation, PCI scoping, consistency choices and failure analysis.

## 7. Common pitfalls

- Treating a PSP timeout as failure and retrying with a new reference (double charge)
- Holding a DB transaction open during the network call
- Publishing to Kafka and writing to the DB as two independent steps
- Mutable `balance` fields with no ledger or audit trail
- Using floating point for money (use integer minor units + currency)
- Skipping reconciliation, so silent mismatches pile up
