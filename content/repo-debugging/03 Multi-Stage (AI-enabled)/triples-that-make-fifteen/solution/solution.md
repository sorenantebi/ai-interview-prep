# Triples That Make Fifteen - Solution

## Root causes / approach

**Stage 1: `cardgame/cards.py`, `rank_value`.** The value of a rank is derived from its position in `RANKS` (`index + 1`), and everything from the face cards onward is capped at 10. The cap was written as `index > 10`, but the jack sits at index 10 (ace is index 0), so the first face card slips through with `10 + 1 = 11` points. Queens and kings (indexes 11 and 12) are capped correctly, which is why only jacks are wrong. The fix is `index >= 10`. The symptoms show up in `hand_total`, `is_bust` and any triple search that includes a jack: a hand such as `JH QS` totals 21 instead of 20, and `JH 4S AD 9C` has no 15 because the jack counts 11.

**Stage 2: `find_triple_sum` in `cardgame/rules.py`.** Group the cards by value (`value -> list of cards`). Iterate over value pairs `a <= b` among the distinct values present, and compute `c = target - a - b`. Require `c >= b` so each multiset of values is visited once, and `c` must be present. Because the same value can be needed up to three times, check `Counter((a, b, c))` against the group sizes. That guarantees three distinct positions and rejects reusing one card (for example `5H 5S 9D` must not return `5+5+5`). Then take the needed number of cards from each group. The result is a tuple of real `Card` objects from the hand, and it works for any iterable (`Hand` included).

**Stage 3: `count_triples_sum`.** The naive approach checks every triple of positions: O(n^3) comparisons, or O(n^2) with a hash of pair sums. Neither survives n = 100,000. Cards are worth only 1-10 points, so count them by value first: `Counter(card.value for card in cards)` is O(n). Then enumerate value multisets `a <= b <= c` with `a + b + c == target` (at most about 10 * 10 pairs) and add up the number of ways to choose positions:
- all three values distinct: `n_a * n_b * n_c`
- `a == b != c`: `C(n_a, 2) * n_c`
- `a != b == c`: `n_a * C(n_b, 2)`
- `a == b == c`: `C(n_a, 3)`

Complexity goes from O(n^3) (or O(n^2)) to O(n + k^2), where k <= 10 is the number of distinct values, so the time is dominated by reading the cards once. Python integers are arbitrary precision, so counts like `C(100000, 3)` are exact; the hidden tests check this.

## How to find it

1. Run the visible tests. `test_face_cards_are_worth_ten` fails with the message naming `JH`, while `QH` and `KH` are fine. That narrows it to one rank, not to all face cards.
2. Print `[(r, rank_value(r)) for r in RANKS]`. The jack comes out as 11, which points at the cap in `rank_value`. The condition compares an index (0-based) with a threshold written as a value.
3. After the fix, the totals and bust tests pass. The remaining failures are `NotImplementedError` from the two stubs in `rules.py`.
4. For stage 2, write down the requirements the tests imply: three distinct positions, `None` otherwise, any iterable input.
5. For stage 3, ask how many different values a card can have. A small answer means counting per value beats looking at the cards one by one. Validate against a brute force `itertools.combinations` on small random hands before trusting the formula, especially the cases with repeated values.
