---
topic: "Fintech"
difficulty: Hard
problem: "Payment System"
---
# Design a Payment System

**Topic:** Fintech · **Difficulty:** Hard · **Answer:** Payment System - Solution

## Prompt

Design a payment system like Stripe or Adyen that lets merchants accept card payments from customers. A merchant's checkout calls our API to charge a customer; we talk to external payment providers and card networks, record the money movement, and notify the merchant. Money must never be lost, duplicated or created out of thin air.

## Requirements to pin down (ask the interviewer)

- Pay-in only, or also payouts to merchants and refunds? Which payment methods (cards, bank transfer, wallets)?
- Are we the PSP (talking to card networks/acquirers) or do we wrap an external PSP?
- Is auth + capture in one step or separate? Multi-currency?
- Audit and compliance needs (PCI DSS, reconciliation with banks)?

## Scale hints

- ~1M payments/day average, ~100 TPS average and 1,000+ TPS at peak (Black Friday)
- External calls are slow (1-3 s) and sometimes time out or return ambiguous results
- Correctness and auditability beat raw throughput; availability still matters
- Merchants retry on network errors, so duplicate requests are guaranteed

## Think about before opening the answer

1. What are the core entities and the payment lifecycle (states and transitions)?
2. How do you make `POST /payments` safe to retry without charging twice?
3. What do you do when the call to the PSP times out and you do not know if the card was charged?
4. How do you record money movement so it can be audited and balanced?
5. How do you notify the merchant reliably, and how do you check that your books match the bank's?
6. How do you keep card numbers out of most of your system?

## Self-check

- [ ] I can explain idempotency keys end to end (API, DB unique constraint, PSP call)
- [ ] I can draw the payment state machine and handle async/ambiguous outcomes
- [ ] I can explain double-entry ledger and why it is append-only
- [ ] I can describe the outbox pattern and reconciliation as the safety nets
