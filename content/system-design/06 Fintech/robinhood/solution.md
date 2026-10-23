---
topic: "Fintech"
difficulty: Hard
problem: "Robinhood"
---
# Design Robinhood (Retail Stock Trading App) – Solution

**Topic:** Fintech · **Difficulty:** Hard · **Question:** Robinhood - Question

## 1. Requirements

**Functional**
- View live quotes and price charts; manage watchlists
- Place, view and cancel orders (market and limit; buy and sell)
- See portfolio: positions, buying power, order history

**Non-functional**
- **Correctness of money and positions:** no overspending, no order lost or duplicated at the exchange
- Low-latency quote streaming (< 1 s) to millions of concurrent clients
- Order placement p99 < 500 ms to acknowledgement; high availability during market hours
- Full audit trail for regulators; eventual consistency allowed for charts and watchlists

**Out of scope:** the exchange matching engine itself, clearing and settlement internals, margin and options, KYC onboarding.

## 2. Back-of-envelope

- Market data: ~10K symbols; a busy symbol ticks ~100/s; total ~50K-200K ticks/s at peaks. Tick ~50 B ⇒ ~10 MB/s inbound. Small.
- Fan-out is the real cost: 5M connected users × ~10 watched symbols. If we conflate to 1 update/s/symbol, per-user fan-out would still be 5M × 10 = **50M pushes/s**; so group by symbol and let each gateway node subscribe once per symbol and broadcast to its local connections (see 5.1).
- Connections: 5M WebSockets ÷ ~100K per node ≈ **~50 gateway nodes**.
- Orders: 1M/day ≈ 12/s average, ~500/s peak at open: tiny for Postgres. The challenge is correctness and exactly-once routing, not throughput.
- Storage: orders+fills ~2 KB × 1M/day ≈ 2 GB/day ≈ 0.7 TB/year; ticks/candles: store 1-min OHLC bars per symbol (10K × 390 min/day ≈ 4M rows/day) rather than raw ticks for charts.

## 3. Core entities and API

Entities: `Account { id, userId, cash, buyingPower }`, `Position { accountId, symbol, qty, avgCost }`, `Order { id, accountId, symbol, side, type, qty, limitPrice, status, clientOrderId, filledQty }`, `Fill { id, orderId, qty, price, venue, ts }`, `Watchlist { userId, symbols[] }`.

```
WS   /stream   subscribe {symbols:[...]}      -> push {symbol, price, ts}   (throttled/conflated)
GET  /quotes?symbols=AAPL,MSFT                -> latest prices
GET  /charts/{symbol}?range=1D                -> OHLC candles
POST /orders   { symbol, side, type, qty, limitPrice? }  Idempotency-Key -> { orderId, status: PENDING }
DELETE /orders/{id}                           -> cancel request
GET  /portfolio                               -> positions, buying power, open orders
```

## 4. High-level design

!Robinhood - Diagram.excalidraw

Two largely independent paths:
- **Market data path (read-heavy, eventually consistent):** exchange/SIP or vendor feeds → **Market Data Ingest** normalizes ticks → **Redis** keeps the latest quote and pub/sub channels per symbol → **Quote Service** gateways push to clients over WebSocket. Candles are aggregated and stored in a time-series DB.
- **Order path (write-critical, strongly consistent):** **Order Service** validates and reserves buying power/shares in **Postgres** in one transaction, writes the order as `PENDING_NEW`, publishes to **Kafka**; the **Order Router** sends it to the venue over FIX and writes back status and fills.

## 5. Deep dives

### 5.1 Streaming prices to millions of clients

- Clients connect to **WebSocket gateways**, each keeping a map `symbol → local connections`. A gateway subscribes to the Redis/Kafka channel of a symbol only if at least one local client watches it, so there are ~10K subscriptions per node at most, regardless of user count.
- **Conflation:** if a symbol ticks 100 times/s, push only the latest price every 250-1000 ms. Slow clients get the latest value, never a backlog (drop-old policy). Mobile on the background gets no push.
- Reconnect storms at market open: connect with jittered backoff; make gateways stateless so clients can hit any node; the client fetches a snapshot via `GET /quotes` and then follows the stream.
- Rejected: polling REST every second from 5M clients (5M req/s, wasteful), and a per-user fan-out in the backend.

### 5.2 Order lifecycle and idempotent routing

!Robinhood - Deep Dive Diagram.excalidraw

States: `PENDING_NEW → ACCEPTED (venue ack) → PARTIALLY_FILLED → FILLED`, plus `CANCEL_PENDING → CANCELED`, `REJECTED`, `EXPIRED`.

- Create: in **one Postgres transaction**, check and reserve (5.3), insert the order with a unique `(accountId, clientOrderId)` (idempotency) and an **outbox** row; commit; ack the user as `PENDING`.
- The outbox relay publishes to Kafka keyed by `accountId` (or `symbol`), so one account's orders stay ordered. The **Router** consumes, sends a FIX `NewOrderSingle` using our `orderId` as `ClOrdID`. The venue **deduplicates by ClOrdID**, so a redelivery after a crash does not create a second order.
- Venue messages (ack, partial fill, fill, reject, cancel ack) arrive as execution reports; each is applied idempotently by `execId` and updates order status, `filledQty` and the `Fill` table, then triggers a position update. Push the status to the client.
- **No answer from the venue:** the order stays `PENDING_NEW`/unknown; query order status by `ClOrdID` (FIX order status request), and run an end-of-day reconciliation with the broker's/clearing house's records. Never assume "no reply = not executed".
- Cancel is a *request*; the order may already be filled. The final state comes from the venue.

### 5.3 Buying power and position safety under concurrency

- Buying order: reserve `qty × limitPrice` (or an estimate plus a collar for market orders) from `buyingPower`: `UPDATE accounts SET buying_power = buying_power - :x WHERE id = :a AND buying_power >= :x`. Atomic and race-free; two concurrent orders cannot both pass.
- Sell order: `UPDATE positions SET reserved = reserved + :q WHERE ... AND qty - reserved >= :q`. This blocks short-selling or selling the same share twice.
- On fill, convert the reservation into actual cash/position changes (and refund the price improvement difference); on cancel/reject, release it. All changes are **ledger entries** (append-only) so balances can be rebuilt and audited.
- Per-account serialization is enough (accounts are independent): shard Postgres by `accountId`; no cross-shard transactions needed on the order path.
- Pre-trade risk checks: price collars, max order size, pattern-day-trader rules, market-hours calendar, and a global kill switch.

### 5.4 Market data and charts

- Latest quote: Redis `HSET quote:{sym}`; no DB read per request. Cache 1D chart data per symbol in Redis; build candles with a stream processor (Flink/Kafka Streams) into **TimescaleDB** or ClickHouse (1m, 5m, 1d rollups).
- Feeds can lag, duplicate or arrive out of order: tag by sequence number/timestamp, drop stale ticks, and show "delayed" if a feed stalls. Use two redundant feed sources and fail over.

### 5.5 Consistency and failure modes

| Data | Consistency | Store |
|---|---|---|
| Orders, balances, positions, fills | Strong, ACID | Postgres (sync replica, PITR) |
| Quotes, charts, watchlists | Eventual, stale ok | Redis, TimescaleDB, cache |
| Order events | At-least-once + idempotent consumers | Kafka |

- Router crash: Kafka offset commits only after the venue ack is persisted; restarts replay safely thanks to `ClOrdID` dedup.
- Venue outage: fail over to another broker/market maker if the first is known down; otherwise queue and reject new orders with a clear message rather than guess.
- At market open, protect order APIs with rate limiting and priority for cancels; shed non-critical reads (charts) before orders.
- End-of-day: reconcile fills, positions and cash with the broker/clearing records and open breaks for manual review.

## 6. What interviewers look for

- **Junior:** separate quote streaming from orders, WebSockets, basic order table and API.
- **Mid:** WebSocket gateways with Redis pub/sub or Kafka, order state machine, async routing via a queue, idempotent order creation.
- **Senior:** per-symbol subscription with conflation, atomic buying power/position reservation, `ClOrdID` dedup with the venue, outbox, unknown-outcome handling, ledger and reconciliation, clear consistency boundaries, regulatory audit trail and kill switches.

## 7. Common pitfalls

- Polling prices from the client or fan-out per user
- Updating quotes through the same database used for orders
- Check-then-update on balance in app code (race, overspend)
- Retrying the order to the exchange without an idempotent client order id
- Treating a timeout as "order failed" and letting the user resubmit
- Using floats for money and prices (use decimals/integers)
- Ignoring reconciliation with the broker and clearing house
