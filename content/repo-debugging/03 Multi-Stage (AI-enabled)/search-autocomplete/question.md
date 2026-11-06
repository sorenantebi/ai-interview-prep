---
difficulty: Hard
kind: multi-stage
---
# Search Autocomplete

**Kind:** Multi-stage (AI-enabled round) · **Difficulty:** Hard

## Scenario
The `autocomplete` package powers the search box of an internal catalogue. Every submitted search is recorded with `AutocompleteService.record`, and as the user types, the UI asks `suggest` for the most popular completions of what has been typed so far. Support has two complaints: searches typed as "New York" or with a tab or stray spacing between words don't behave like their clean lower-case versions, and the completion call itself was never finished. Once it works, the catalogue team wants to load about 100,000 distinct phrases and serve thousands of suggestion requests, with new searches arriving while users are typing.

## Your tasks
1. **Fix the bug.** Phrases and prefixes that differ only in capitalisation or whitespace are not treated as the same thing. Find and fix the cause (the failing tests show the symptoms).
2. **Implement the core feature.** `suggest(prefix, k)` must return up to `k` completions for the prefix, ordered by search count (highest first), with ties broken alphabetically. A phrase equal to the prefix counts as a completion. An empty prefix returns the most popular phrases overall. The index method that does the real work is currently a stub.
3. **Make it fast.** Hidden tests load 10^5 phrases, answer many queries, and interleave new `record` calls with queries, each under a time budget of about one second. A scan over every phrase per query will not make it. Keep results exactly the same as in stage 2.

## Notes
- Entry point: `AutocompleteService` in `autocomplete/service.py`. It normalises text and delegates storage and ranking to `PhraseIndex`, which expects already-normalised keys.
- Python 3 standard library only. Counts only ever increase: `record` adds to the running total of a phrase.
- `suggest` returns `Suggestion` objects (phrase and total count). The default `k` is 5, and `k` may be larger than the number of matches, or larger than whatever you cache.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
