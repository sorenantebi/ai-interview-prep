---
difficulty: Medium
kind: bug-fix
---
# Catalogue cache evicts the wrong products

**Kind:** Bug fix · **Difficulty:** Medium

## Scenario
The product catalogue API keeps recently requested products and category listings in a small in-memory cache so it doesn't hit the backing store on every request. Since the last release, the ops team sees two problems. Popular products keep falling out of the cache even though they are requested constantly. And when a price is changed in one category, products from completely unrelated categories are also dropped and have to be reloaded.

## Your tasks
1. Users report that frequently requested products are evicted while rarely used ones stay cached. Find and fix the cause (the failing tests show the symptoms).
2. Price updates in one category invalidate cache entries that belong to other categories. Find and fix the cause.
3. Make sure all visible tests pass and think about which edge cases the hidden tests might probe (overwriting an existing key, tag handling, entry ordering).

## Notes
- Entry point for the API layer is `CatalogService` in `catalog/service.py`; the cache lives in `catalog/cache.py`.
- Cache entries can carry tags, and `invalidate_tag` removes every entry carrying a given tag.
- Don't change the public method names or signatures; other services call them.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
