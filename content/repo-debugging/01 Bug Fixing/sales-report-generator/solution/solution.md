# Sales Report Generator - Solution

## Root causes / approach
**Bug 1: `salesreport/aggregate.py`, `region_key`.** The function is meant to normalise region names so that spelling variants fall into one group, but it only stripped whitespace. `'EU'` and `'eu'` therefore became different dictionary keys in `group_by_region`, and `region_totals` and the report listed the region twice with split totals. Fix: normalise case as well, `name.strip().upper()`. Because both `group_by_region` and `region_totals` go through `region_key`, one change fixes every consumer, and the report already shows regions in upper case.

**Bug 2: `salesreport/report.py`, `top_seller`.** The ranking sorted by `(total, name)` ascending and returned the first element, which is the rep with the *lowest* total. Fix: sort by `(-total, name)` so the highest total comes first and ties are still broken alphabetically. Using `-total` instead of `reverse=True` is deliberate: `reverse=True` would also reverse the name order and break the alphabetical tie-break. The visible tie test passed even with the bug, which is why the tie rule needs care when fixing.

## How to find it
1. Run the tests. Two groups fail: `test_group_by_region_merges_spelling_variants` / `test_region_totals` / `test_full_report` (regions) and `test_top_seller_is_highest` (ranking).
2. For the region failures, print `group_by_region(parse_sales(CSV)).keys()`. You will see `['EU', 'eu', 'US', 'us']`, which points straight at the key function used for grouping (`region_key`).
3. For the top-seller failure, print `rep_totals(...)` (correct: Carol has 300) and then the sorted list in `top_seller`. The sort is ascending and the first element is taken, so the result is the minimum.
4. Check the parser last: it was not at fault, since the tests that only parse (`test_parser.py`) all pass. That narrows the search to aggregation and reporting.
