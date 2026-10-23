---
topic: "Messaging & Real-time"
difficulty: Medium
problem: "Online Chess"
---
# Design Online Chess – Solution

**Topic:** Messaging & Real-time · **Difficulty:** Medium · **Question:** Online Chess - Question

## 1. Requirements

**Functional**
- Matchmaking: pick a time control and be paired with a player of similar rating
- Play a game: make legal moves, offer draw, resign; the game ends on mate, draw, resignation or timeout
- Both players see moves in real time; clocks are consistent
- Store finished games (PGN) for replay; update ratings (Elo/Glicko)
- Spectate live games; reconnect after a drop

**Non-functional**
- Move latency < 200 ms; **no illegal moves or clock tampering** (server authoritative)
- No game state lost on server failure; highly available matchmaking
- ~1M concurrent games

**Out of scope:** anti-cheat engines, tournaments, in-game chat details, puzzles.

## 2. Back-of-envelope

- 1M concurrent games = 2M WebSocket connections → ~20-40 gateway servers at 50-100K each (plus headroom).
- A game of 80 half-moves over ~10 min ≈ 0.13 moves/s per game → **~130K moves/s** system-wide. Trivial throughput; the hard parts are correctness and latency.
- Game record: ~80 moves × ~6 B (SAN) + metadata ≈ 1 KB. 10M games/day → 10 GB/day, ~3.6 TB/year. Fits Postgres with partitioning (or object storage for old PGNs).
- Live state: board FEN (~90 B) + move list + clocks ≈ 1-2 KB × 1M games = **~2 GB in Redis**. Tiny.

## 3. Core entities and API

Entities: `User { userId, rating }`, `Game { gameId, whiteId, blackId, timeControl, status, result, pgn }`, `Move { gameId, ply, san, ts }`.

```
POST /matchmaking/join   { timeControl, ratedMode }   -> queued (or pushed over WS on match)
WS   /games/{gameId}
  -> { type: "move", ply, from, to, promotion? }      client move (ply = expected move number)
  <- { type: "move", ply, san, clocks }                server-validated move for both players
  -> { type: "resign" | "offerDraw" | "acceptDraw" }
  <- { type: "gameOver", result, reason }
GET  /games/{gameId}     -> game record / PGN
```

## 4. High-level design

!Online Chess - Diagram.excalidraw

- Players connect to a **WebSocket gateway** (stateful, holds sockets).
- **Matchmaking** keeps waiting players in a Redis sorted set per time control, scored by rating, and creates a game when it finds a close pair.
- The **Game Service** owns a game: it validates each move with a chess library, updates the live state in Redis and pushes the result to both players (and spectators) via the gateway.
- When a game ends, an event goes to Kafka; a worker writes the archive and updates ratings in Postgres.

## 5. Deep dives

### 5.1 Server authority and the clock

- The client sends **intent** (`from`, `to`). The server checks turn order, legality (check, castling rights, en passant, promotion), expected `ply` (rejects a stale or duplicate move) and then applies it. Never trust the client for legality or time.
- **Clock:** store `whiteRemaining`, `blackRemaining`, `lastMoveTs`, `sideToMove` using the server clock. On a move, `remaining -= now - lastMoveTs`, then add the increment. Clients render a local countdown only for display and re-sync from each server message.
- **Latency compensation:** optionally credit up to ~100 ms based on measured RTT so high-latency players are not penalised, bounded to prevent abuse.
- **Timeout detection:** no polling of all games. Schedule a timer at `now + remaining` (an in-memory timer wheel on the owning server, or a Redis ZSET of deadlines scanned by a small worker). A move cancels or reschedules it.

### 5.2 Routing moves between servers

| Option | Notes |
|---|---|
| **Game owned by one Game Service instance** (consistent hash on `gameId`) | Serialises moves for the game, so no races; gateway forwards both players' moves to the owner. Chosen |
| Both clients on the same gateway | Impossible to guarantee |
| Pub/sub channel per game (Redis) between gateways | Good for delivery to spectators and to the opponent's gateway; used *after* the owner validates |
| Optimistic concurrency only (no owner) | Works with a Redis version/CAS check, simpler failover, slightly more contention |

Flow: Gateway → owner Game Service → validate → write state to Redis (`WATCH`/Lua CAS on `ply`, so a duplicate or racing move loses) → publish `move` to the game channel → gateways relay to White, Black and spectators.

### 5.3 Matchmaking

- Per (time control, mode) a **Redis ZSET** of `userId` scored by rating, with the join timestamp.
- A matcher loop (or the join call itself) queries `ZRANGEBYSCORE rating-δ rating+δ`, picks the best candidate, removes both atomically (Lua script) and creates the game. **The rating window widens** with wait time (e.g. ±50 initially, +25 every 3 s) so nobody waits forever.
- Atomic removal avoids pairing one player twice. Colour assignment alternates/balances against previous games.
- Sharding: by time control (naturally separate pools); at larger scale, shard by rating band with adjacent-band lookups.
- Alternatives: DB table polling (slow, contention), Kafka pairing (overkill and awkward to dequeue by rating).

### 5.4 State, persistence and recovery

- **Live state in Redis:** `game:{id} → {fen, moves, clocks, version, status}` with TTL after the game ends. Moves also appended to a Redis stream/list for spectators who join late (replay then follow).
- Because state is externalised, a Game Service crash loses nothing: the new owner reloads from Redis and clocks resume (clock is derived from timestamps, not an in-memory counter).
- **Archive:** at game end publish `GameFinished` to Kafka. A worker writes the PGN and result to Postgres (`games` partitioned by month) and updates ratings. Idempotent by `gameId` (unique key) so retries are safe.
- **Ratings:** Elo (`R' = R + K(S - E)`) or Glicko-2 with rating deviation; updating in the worker keeps the hot path free. A cheap per-user lock/version prevents two simultaneous games clobbering each other's rating (or process by user partition in Kafka).

### 5.5 Disconnects, spectators, abuse

- **Disconnect:** heartbeats every ~5 s. If a player is gone, their clock keeps running; they can reconnect to the same `gameId` (resume gives full state). A longer grace window (~30-60 s) may allow "abandon → opponent can claim win".
- **Spectators:** subscribe to the game channel via the gateway, and get the move list on join. Broadcasting 1 move per few seconds is cheap, but add a delay (e.g. 30-60 s) for cheating-prone broadcasts, and cache hot games (top-board) at the CDN/edge via SSE.
- **Cheating:** engine assistance is detected offline from the archived PGN (compare to engine best moves) by async workers, which is why the archive pipeline matters. Rate limit connections and moves.

### 5.6 Failure modes

- Gateway crash: clients reconnect to another gateway (game state is not in the gateway).
- Redis failure: live games are not in Postgres until they finish, so run Redis replicated across AZs with AOF and also append each move to a Kafka log; on total loss, replay the log to rebuild in-flight games.
- Duplicate message from client retry: rejected by the `ply` check.
- Matchmaking pool loss: players simply re-queue; low impact.

## 6. What interviewers look for

- **Junior:** WebSockets for moves, server stores the game, simple matching.
- **Mid:** server-authoritative validation and clocks, Redis for live state, rating-window matchmaking, async archive.
- **Senior:** ownership/serialisation of moves per game, CAS on `ply`, timer design for flag detection, matchmaking atomicity and window widening, recovery from failures without in-memory state, rating pipeline idempotency, spectator and anti-cheat handling.

## 7. Common pitfalls

- Trusting the client for move legality or the clock
- Running the clock only in server memory (lost on restart) or counting on client time
- Scanning all waiting users to find a match
- Writing every move synchronously to Postgres on the hot path
- No handling for disconnects, duplicate moves or racing resign/move
- Over-designing with microservices for ~130K moves/s
