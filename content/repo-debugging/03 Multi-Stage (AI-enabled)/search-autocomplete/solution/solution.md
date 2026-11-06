# Search Autocomplete - Solution

## Root causes / approach

**Stage 1 - `autocomplete/text.py`, `normalize`.**
The function starts with a "fast path": if the text has no leading or trailing whitespace and no double space, it returns the input untouched. That path skips both the `.lower()` call and the whitespace collapsing. Clean-looking input like `"New York"` therefore keeps its capitalisation, and `"new\tyork"` keeps its tab (a single tab is not a double space). Phrases were stored and looked up under different keys depending on how they were typed, which explains both the case and the whitespace symptoms. Only input that happened to contain extra spaces went through the correct path. The fix is to delete the fast path so every non-empty input goes through `strip`, the whitespace collapse and `lower`.

**Stage 2 - `PhraseIndex.top_k`.**
The simple version scans every stored phrase, keeps those with `phrase.startswith(prefix)`, and returns `heapq.nsmallest(k, [(-count, phrase), ...])`. Sorting on `(-count, phrase)` gives "count descending, ties alphabetical" with no custom comparator. This is O(N) per query. It is correct and passes all the visible tests, but it is far too slow for 10^5 phrases and thousands of queries.

**Stage 3 - trie with cached top-k.**
`PhraseIndex` keeps the `_counts` dict (for `count`, `__len__` and `__contains__`) and adds a trie. Every node stores `top`, a sorted list of the best `CACHE_SIZE` (10) `(-count, phrase)` entries in its subtree.
- `add` walks the phrase once and updates the `top` list of every node on the path, root included, so the empty prefix works. Because counts only increase, an updated phrase can only move up. For each node the code removes the phrase's old entry if present, inserts the new one with `bisect.insort`, and trims to `CACHE_SIZE`. If the list is full and the new entry ranks below the last one, the phrase cannot be in the list and the node is skipped. That makes `add` O(L * CACHE_SIZE), where L is the phrase length.
- `top_k` walks the prefix (O(len(prefix))) and slices the node's cached list. Queries with `k` above the cache size fall back to walking the subtree and using `heapq.nsmallest`. If the cached list is shorter than `CACHE_SIZE`, it already holds every phrase in the subtree and can be sliced directly.

Complexity: query goes from O(N) to O(len(prefix) + k). Insert and count update go from O(1) to O(L * CACHE_SIZE). Memory is O(total characters) for the nodes, plus at most `CACHE_SIZE` tuples per node. A common alternative is to invalidate cached nodes on write and recompute lazily, but that recomputes huge subtrees near the root after every write and fails the interleaved test. Updating the cache eagerly on `add` avoids that. It fits the existing design: the service is unchanged and only `PhraseIndex` changes.

## How to find it

- Start with `tests/test_text.py::test_lowercases` and `test_collapses_whitespace_between_words`. Call `normalize` directly with a few inputs: `"New York"`, `"new\tyork"`, `"new  york"`, `" New York"`. The inputs that come back wrong (clean-looking ones) while the "messy" ones come out right point to an early return in `normalize`.
- Read `normalize` top to bottom and ask which inputs never reach the `sub(...).lower()` line.
- For stage 2, the failing index tests raise `NotImplementedError`; read the docstring of `top_k` for the exact ordering contract and write the tuple-key version first.
- For stage 3, profile mentally: queries times phrases. Time a few queries on a generated 10^5-phrase index to confirm the scan is the bottleneck, then design the cache so writes stay cheap, since hidden tests interleave `record` and `suggest`.
