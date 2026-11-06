---
difficulty: Easy
kind: bug-fix
---
# Ledger Interest, Fees and Statements

**Kind:** Bug fix · **Difficulty:** Easy

## Scenario
`ledger` is a small library that a retail-banking back office uses to post transactions to accounts, accrue monthly interest, charge fees, and produce monthly statements. All money is stored as integer cents. Support has received several complaints: interest credited to some accounts is a few cents too low, wire-transfer fees are off by one cent for certain amounts, and the totals printed on monthly statements don't match what customers add up themselves.

## Your tasks
1. Customers with larger balances say their monthly interest is slightly lower than their own calculation. Find and fix the cause (the failing tests in `tests/test_interest.py` show the symptoms).
2. Wire-transfer fees are sometimes one cent lower than the published fee schedule says. Find and fix the cause.
3. Monthly statements show a wrong net change and closing balance. Find and fix the cause.
4. Make sure the visible tests pass without changing the tests, and think about which edge cases the hidden tests might cover.

## Notes
- Entry points: `ledger.interest.accrue_monthly`, `ledger.fees.wire_fee_cents`, `ledger.statement.build_statement`.
- All amounts are integer cents. Whenever a result is rounded, the convention is round half up (half away from zero for negatives), and `ledger/money.py` is where shared money helpers live.
- Interest uses a 365-day year and a balance snapshot taken at the end of the day before the month starts.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
