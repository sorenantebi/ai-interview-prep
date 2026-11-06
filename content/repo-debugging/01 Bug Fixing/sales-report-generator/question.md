---
difficulty: Easy
kind: bug-fix
---
# Sales Report Generator

**Kind:** Bug fix · **Difficulty:** Easy

## Scenario
`salesreport` turns a CSV export of sales (region, rep, amount) into a short plain-text report for the weekly sales meeting: totals per region and the top-selling rep. After the latest export, the sales team complained that regions show up twice in the report, with the totals split between them, and that the "Top seller" line names the person who sold the least.

## Your tasks
1. Users report that the same region appears more than once in the report with its sales divided between the entries. Find and fix the cause (the failing tests show the symptoms).
2. Users report that the "Top seller" line names the wrong rep. Find and fix the cause.
3. Make sure all visible tests pass without changing the tests, and think about which edge cases the hidden tests might cover (blank rows, negative amounts, ties, odd spacing).

## Notes
- The entry point is `build_report(csv_text)` in `salesreport/report.py`; it takes the CSV content as a string and returns the report text.
- Parsing lives in `salesreport/parser.py`, grouping and totals in `salesreport/aggregate.py`.
- Region names in exports are not consistently written (different capitalisation, stray spaces); the report shows them in upper case.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
