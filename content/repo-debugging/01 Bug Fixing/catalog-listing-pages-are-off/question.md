---
difficulty: Easy
kind: bug-fix
---
# Catalog listing pages are off

**Kind:** Bug fix · **Difficulty:** Easy

## Scenario
The `catalog` package backs a small REST-style endpoint that lists product records, with optional category filtering, sorting and pagination. The mobile team reports that the first page of results is missing the first items and appears to start at the second page. The "load more" button also keeps showing after the final page whenever the number of items is an exact multiple of the page size. Separately, listings sorted by price do not come back in price order.

## Your tasks
1. Users report that page 1 does not start with the first record, and that "has next page" is wrong on the last page in some cases. Find and fix the causes (the failing tests show the symptoms).
2. Sorting by price returns records in the wrong order. Find and fix the cause.
3. Make sure all tests in `tests/` pass, and think about boundary cases (exact multiples of the page size, pages past the end, an empty result set) before you submit.

## Notes
- The entry point is `list_records(repo, query)` in `catalog/handlers.py`. It takes a `RecordRepository` and a dict of query-string parameters, and returns a `(status_code, body)` tuple.
- Pages are 1-based. The default page size is 10 and the maximum is 50.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
