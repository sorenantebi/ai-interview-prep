from datetime import date

from ledger.interest import accrue_monthly, interest_for_period
from ledger.models import Account, Transaction


def test_no_interest_on_zero_or_negative_balance():
    assert interest_for_period(0, 450, 30) == 0
    assert interest_for_period(-50_000, 450, 30) == 0


def test_one_day_of_interest():
    assert interest_for_period(1_000_000, 450, 1) == 123


def test_thirty_days_of_interest():
    # $10,000.00 at 4.50% for 30 days is $36.99 (36.986...)
    assert interest_for_period(1_000_000, 450, 30) == 3699, "expected 3699 cents"


def test_accrue_monthly_uses_balance_at_month_start():
    acct = Account("A-1", annual_rate_bps=450, opening_balance_cents=500_000)
    acct.post(Transaction(date(2025, 3, 20), 500_000, "salary"))
    acct.post(Transaction(date(2025, 4, 10), 900_000, "bonus"))
    assert accrue_monthly(acct, 2025, 4) == 3699
