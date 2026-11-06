---
difficulty: Medium
kind: multi-stage
---
# Triples That Make Fifteen

**Kind:** Multi-stage (AI-enabled round) · **Difficulty:** Medium

## Scenario
`cardgame` is the small engine behind a family of "fifteen" card games: it builds and deals decks, parses hands written in short notation (`"KH 5S 10D"`), and applies scoring rules. Players have reported that some hands containing face cards are scored incorrectly. The game designers also want two new rules built on top of the engine: spotting a "fifteen" (three cards that add up to 15) and counting every one in a hand. The counting rule has to cope with the huge multi-deck hands used by the simulation team.

## Your tasks
1. **Fix the bug.** Hand totals and bust checks come out wrong for some hands that contain face cards. Find and fix the cause (the failing tests show the symptoms).
2. **Implement `find_triple_sum(cards, target=15)`** in `cardgame/rules.py`. It returns a tuple of three cards from three different positions in the hand whose values add up to `target`, or `None` if no such triple exists. Any valid triple is accepted.
3. **Implement `count_triples_sum(cards, target=15)`** in `cardgame/rules.py`. It returns how many triples of positions (`i < j < k`) have values adding up to `target`. Hidden tests use hands with 100,000 cards and assert the running time, so a solution that looks at every pair or triple of cards will not finish.

## Notes
- Card values: ace = 1, number cards = face value, J/Q/K = 10. Every card is therefore worth between 1 and 10 points.
- `cards` can be any iterable of `Card` objects, including a `Hand`. Hands may contain equal cards (multi-deck play); two equal cards are still two different cards.
- Python 3 standard library only. Tests are plain `assert` functions in `tests/`.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
