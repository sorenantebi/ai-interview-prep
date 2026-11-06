---
difficulty: Hard
kind: multi-stage
---
# Word Game Helper: Distinct-Letter Selections

**Kind:** Multi-stage (AI-enabled round) · **Difficulty:** Hard

## Scenario
`wordgame` is a small helper library behind a word-puzzle app. Players paste in a list of words, and the app should tell them the largest total length they can reach by picking words so that no letter appears twice across the whole selection. The first beta testers report that some perfectly ordinary lowercase words crash the tool with a `ValueError`. The headline feature, the "best total length" number, has not been written yet, and the product team wants it to stay responsive with word lists of 100,000 entries.

## Your tasks
1. **Fix the bug.** Some valid lowercase words are rejected. Find and fix the cause (the failing tests show the symptoms).
2. **Implement the feature.** `max_unique_length(words)` in `wordgame/solver.py` is a stub. It must return the largest possible total length of a selection of words in which no letter occurs more than once across the selection. Each list entry may be used at most once. Words that repeat a letter themselves are never usable. If nothing is usable, the result is `0`.
3. **Make it fast.** Hidden tests call `max_unique_length` with lists of about 100,000 words (many of them duplicates, anagrams or unusable) and assert it finishes in about a second. Make sure your solution holds up on such inputs.

## Notes
- Entry points: `wordgame.solver.max_unique_length` and `wordgame.report.summarize_text`. The report builds on the solver.
- Words passed to the solver are expected to be already cleaned (lowercase `a`-`z` only). `wordgame.words.clean_words` does that cleaning.
- Only the Python 3 standard library is available.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
