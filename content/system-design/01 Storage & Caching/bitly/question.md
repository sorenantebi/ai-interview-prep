---
video: https://www.youtube.com/watch?v=iUU4O1sWtJA
topic: "Storage & Caching"
difficulty: Easy
problem: "Bitly"
---
# Design Bitly (URL Shortener)

**Topic:** Storage & Caching · **Difficulty:** Easy · **Answer:** Bitly - Solution

## Prompt

Design a URL shortening service like Bitly. Given a long URL, the service returns a short URL (e.g. `short.ly/aZ3x9Q`). Visiting the short URL redirects the user to the original long URL.

## Requirements to pin down (ask the interviewer)

- Can users pick a custom alias? Do links expire (optional expiration date)?
- Do we need analytics (click counts)? Do users have accounts?
- Is the same long URL always mapped to the same short code?

## Scale hints

- ~1B URLs stored in total, ~100M daily active users
- Read:write ratio around 1000:1 (reads dominate)
- Redirect latency target: < 100 ms, availability target 99.99%
- Short codes must never collide, and must be hard to enumerate

## Think about before opening the answer

1. What are the core entities (Original URL, Short URL, User) and the 2 APIs you need?
2. How do you generate short codes that are unique, short and unpredictable?
3. How do you make redirects fast at ~1000x more reads than writes (index, cache, edge)?
4. 301 vs 302: which one and why?
5. What happens when your code generator or database becomes the bottleneck?

## Self-check

- [ ] I can estimate storage (rows × bytes × years)
- [ ] I can compare at least 3 code generation strategies (hash, random + check, counter) and say which is best and why
- [ ] I can explain the caching layer and its failure modes
