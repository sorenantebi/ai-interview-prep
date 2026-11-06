# Catalog listing pages are off - Solution

## Root causes / approach
There are three independent bugs in two files.

1. **`catalog/pagination.py`, `offset_for`**: it returned `page * page_size`, but pages are 1-based. Page 1 therefore started at index `page_size`, which skipped the first page of results, and every later page was shifted by one page as well. Fix: `(page - 1) * page_size`.

2. **`catalog/pagination.py`, `has_more`**: it used `offset + page_size <= total`. On the last page, when the total is an exact multiple of the page size, `offset + page_size == total`, so the check wrongly said there was more. A next page exists only if the end of this page is strictly before the total: `offset + page_size < total`. Partial last pages hid this bug, which is why it only showed up for exact multiples.

3. **`catalog/repository.py`, `SORT_KEYS["price"]`**: the key function sorted by `name.lower()` instead of `price_cents`, so "sort by price" returned name order. Fix: `lambda r: r.price_cents`.

The handler, parameter parsing and models are correct. Bugs 1 and 2 both live in `pagination.py` but in different functions, and bug 2 only becomes visible after bug 1 is fixed, because the shifted offset previously made the last-page tests fail for a different reason.

## How to find it
- Start with `test_first_page_items` and `test_offset_first_page` in `tests/test_pagination.py`. The latter calls `offset_for(1, 10)` directly and gets 10 instead of 0, which points straight at the formula.
- After fixing that, `test_last_full_page_has_no_next` still fails. Print `has_more(10, 10, 20)` and compare it with the boundary: the page covers indices 10..19, so nothing follows. That exposes the `<=`.
- For `test_sort_by_price`, print the prices returned by `repo.query(sort_by="price")`. They are not ascending but the names are, so look at `SORT_KEYS` in `repository.py`.
- When testing pagination, always try the boundary totals (exact multiple, multiple plus one, zero) in addition to a typical value.
