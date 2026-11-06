# Ledger Interest, Fees and Statements - Solution

## Root causes / approach

**1. `ledger/interest.py`, `interest_for_period`: premature integer division.**
The function computed a daily interest amount with floor division (`balance * rate // (10_000 * 365)`) and then multiplied by the number of days. The fractional cent lost each day is multiplied by `days`, and the result is also truncated rather than rounded half up. For $10,000.00 at 4.50% over 30 days the daily figure is 123.28 and gets floored to 123, so the result is 3690 instead of 3699. Larger balances lose more. Fix: multiply everything first and divide once, using the shared helper: `div_round_half_up(balance * rate * days, 10_000 * 365)`.

**2. `ledger/fees.py`, `wire_fee_cents`: float division plus `round()`.**
`round(amount * 50 / 10_000)` goes through a float and Python's `round` uses banker's rounding (half to even). 30,100 cents gives 150.5, which rounds to 150, but the fee schedule (and the project's convention) says half up, so 151. Fix: `div_round_half_up(amount_cents * WIRE_RATE_BPS, 10_000)`, which stays in integers and rounds half up. The min and max clamps are unchanged. The bug is invisible for amounts below about $200, because the $1.00 minimum hides it.

**3. `ledger/statement.py`, `net_total_cents`: off-by-one loop.**
The loop was `range(len(transactions) - 1)`, so the last transaction was never added. The statement's `total_cents` and `closing_balance_cents` were therefore wrong, and a one-transaction statement showed a net change of 0. Fix: iterate over all transactions (`for txn in transactions`).

## How to find it
- Start with `tests/test_statement.py::test_statement_total`. The expected 96,500 versus actual 97,500 is exactly the amount of the last line (-1,000). Combined with the single-transaction test returning 0, this points to the summation helper. Printing `stmt.lines` shows the lines are right, so the problem is in the total.
- For `test_thirty_days_of_interest`, compute the expected value by hand: `1_000_000 * 450 * 30 / 3_650_000 = 3698.63`. The code returns 3690, which is `123 * 30`. That tells you the daily amount was floored before multiplying. `ledger/money.py` already has a half-up helper, which is a hint about the intended convention.
- For `test_wire_fee_half_cent_rounds_up`, print `amount * 50 / 10_000` and notice the exact `.5`. A result one cent low on an exact half points at `round()` using half-to-even. Also note that the tests with smaller amounts pass only because of the minimum fee clamp.
