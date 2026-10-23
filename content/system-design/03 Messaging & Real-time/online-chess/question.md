---
topic: "Messaging & Real-time"
difficulty: Medium
problem: "Online Chess"
---
# Design Online Chess

**Topic:** Messaging & Real-time · **Difficulty:** Medium · **Answer:** Online Chess - Solution

## Prompt

Design a platform like Chess.com or Lichess where two players are matched, play a timed game in real time, and can later review the game. Spectators can watch live games.

## Requirements to pin down (ask the interviewer)

- Which modes: rated and casual, time controls (blitz, rapid)? Play vs friend by link?
- Do we need spectators, chat, and game replay/history?
- Is cheating detection in scope? Reconnecting after a disconnect?
- Do we need to support computer opponents or only humans?

## Scale hints

- ~10M daily active users, ~1M concurrent games at peak
- A game has ~40 moves per player; a move must reach the opponent in < 200 ms
- Matchmaking should find an opponent of similar rating in a few seconds
- Clocks must be fair and cannot be manipulated by the client

## Think about before opening the answer

1. Who is the source of truth for the board and for the clock, client or server?
2. How do two players, connected to different servers, exchange moves?
3. How do you pair players by rating and time control without scanning every waiting user?
4. What happens on disconnect, on timeout, and when two moves race?
5. What do you persist, when, and how do you update ratings?
6. How would you add spectators with minimal extra load?

## Self-check

- [ ] I can justify server-authoritative validation and clocks
- [ ] I can design a matchmaking pool with rating windows
- [ ] I can explain game state storage and how a game service restarts without losing games
- [ ] I can describe the post-game pipeline (archive and rating update)
