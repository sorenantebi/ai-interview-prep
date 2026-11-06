# Word Game Helper: Distinct-Letter Selections - Solution

## Root causes / approach

**Stage 1: `wordgame/bitmask.py`, `_BITS` lookup table.** The table mapping letters to bits was built with `range(ALPHABET_SIZE - 1)`, so it covered only `a`-`y`. `z` was missing from the table, `letter_mask` saw `None` for it and raised `ValueError` for any word containing `z`. Words without a `z` worked, which is why the bug looked intermittent. Fix: `range(ALPHABET_SIZE)`.

**Stage 2: `wordgame/solver.py`, `max_unique_length`.** The design reuses the existing helpers. `usable_masks` already drops words that repeat a letter and `letter_mask` gives each word a bitmask. Two words can be combined exactly when `a & b == 0`. A set `reachable` holds the letter masks of every valid selection found so far, starting with `{0}` (the empty selection). For each word mask, every reachable mask that does not overlap with it yields a new reachable mask `taken | mask`. Because all letters in a selection are distinct, the total length is just `popcount(mask)`, so the answer is the maximum popcount in `reachable`. Iterating over a snapshot (`list(reachable)`) ensures each word is used at most once.

**Stage 3: making it fast.**
- A naive approach (recursion over words, or a reachable-set DP over all 100,000 entries) repeats the same work for duplicates and anagrams. A backtracking search over all words is exponential. The DP without dedupe costs `O(n * |reachable|)`.
- The fix is to dedupe. `set(words)` collapses identical strings before any mask is computed, and `set(usable_masks(...))` collapses anagrams. Masks that are `0` (empty words) are discarded, since they add nothing. The DP then costs `O(d * |reachable|)` where `d` is the number of distinct masks. The number of distinct masks is at most `min(n, 2^26)` and in practice small, and `|reachable|` is bounded by the number of pairwise-disjoint combinations. On the hidden inputs this is well under a tenth of a second against many seconds for the naive version.
- Further pruning is possible (for example a depth-first search with an upper bound of `popcount(current | union_of_remaining)`, or an early exit once all 26 letters are used), but dedupe plus the reachable-set DP is enough here. Be aware that a pool of many tiny masks (for example all 26 single letters) makes `reachable` grow to `2^26`. The tests avoid that case; a bounded DFS is the better tool for it.

## How to find it
1. Run the visible tests. `test_letter_mask_basic` and `test_letter_mask_single_letter` fail with a `ValueError` on a plain lowercase word. The first assertion that breaks is the one involving `z`.
2. Print `letter_mask(ch)` for each letter of the alphabet. Only `z` raises, which points straight at the lookup table in `bitmask.py`, and its range is the suspect.
3. For the stub, read `usable_masks` and `popcount` first: the helpers hint at the intended design (masks plus disjointness checks).
4. For the performance stage, think about what a 100,000-word list really contains: duplicates, anagrams and unusable words. Count the distinct masks (print `len(set(usable_masks(words)))`) and you will see the DP only needs to run over a few dozen values.
