---
difficulty: Hard
kind: bug-fix
---
# Spreadsheet Formula Evaluator Returns Wrong Results

**Kind:** Bug fix · **Difficulty:** Hard

## Scenario
The `formula` package powers the calculated cells of an internal spreadsheet tool. Users type formulas such as `=A1 - B1 - 3` or `=SUM(A1, B1) * -2`, and the sheet shows the result. After a recent refactor, support has collected several complaints: some totals are simply wrong, some formulas that used to work are now rejected with an error, and some formulas that mention cells silently produce numbers that don't match the cell contents. The failing tests show the symptoms.

## Your tasks
1. Users report that chained subtractions such as `10 - 4 - 3` give a different total than a calculator would. Find and fix the cause.
2. Users report that formulas containing a negative number written right after an operator (for example `3 * -2` or `5 - -3`) are rejected, although `-2 * 3` works. Find and fix the cause.
3. Users report that formulas typing a cell reference in lowercase (for example `a1 + b1`) return numbers that don't match the cells, and no error is shown. Find and fix the cause.
4. Make all tests in `tests/` pass without changing the tests, and check that the hidden edge cases (mixed case, long subtraction chains, circular references, error handling) behave sensibly.

## Notes
- The public entry point is `formula.Sheet`: `set(ref, content)`, `value(ref)` and `evaluate(formula)`. The pipeline is `tokenizer.py` → `parser.py` → `evaluator.py`, with `sheet.py` supplying cell values.
- All numbers are handled as floats. Empty cells count as `0`.
- Function names (`SUM`, `MIN`, `MAX`, `AVG`) and cell references are meant to be case-insensitive.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
