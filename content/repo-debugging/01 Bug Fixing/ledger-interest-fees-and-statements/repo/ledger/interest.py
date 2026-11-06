"""Interest accrual on account balances."""

import calendar
from datetime import date, timedelta

from ledger.models import Account

DAYS_IN_YEAR = 365
BPS_DENOMINATOR = 10_000


def interest_for_period(balance_cents: int, annual_rate_bps: int, days: int) -> int:
    """Simple interest in cents for ``days`` days at ``annual_rate_bps``
    basis points per year. Non-positive balances earn nothing."""
    if balance_cents <= 0 or days <= 0:
        return 0
    daily = balance_cents * annual_rate_bps // (BPS_DENOMINATOR * DAYS_IN_YEAR)
    return daily * days


def accrue_monthly(account: Account, year: int, month: int) -> int:
    """Interest earned by ``account`` over the given calendar month.

    The balance used is the one at the end of the day before the month starts.
    """
    first_day = date(year, month, 1)
    days = calendar.monthrange(year, month)[1]
    balance = account.balance_as_of(first_day - timedelta(days=1))
    return interest_for_period(balance, account.annual_rate_bps, days)
