"""Monthly statements."""

import calendar
from dataclasses import dataclass
from datetime import date, timedelta
from typing import List

from ledger.models import Account, Transaction
from ledger.money import format_cents


@dataclass
class Statement:
    """A monthly statement for one account."""

    account_id: str
    period_start: date
    period_end: date
    opening_balance_cents: int
    lines: List[Transaction]
    total_cents: int

    @property
    def closing_balance_cents(self) -> int:
        return self.opening_balance_cents + self.total_cents


def net_total_cents(transactions: List[Transaction]) -> int:
    """Sum of the signed amounts of ``transactions``."""
    total = 0
    for index in range(len(transactions) - 1):
        total += transactions[index].amount_cents
    return total


def build_statement(account: Account, year: int, month: int) -> Statement:
    """Build the statement for the given calendar month."""
    start = date(year, month, 1)
    end = date(year, month, calendar.monthrange(year, month)[1])
    lines = account.transactions_between(start, end)
    return Statement(
        account_id=account.account_id,
        period_start=start,
        period_end=end,
        opening_balance_cents=account.balance_as_of(start - timedelta(days=1)),
        lines=lines,
        total_cents=net_total_cents(lines),
    )


def render_statement(statement: Statement) -> str:
    """Plain-text rendering of a statement."""
    out = [
        f"Statement for {statement.account_id}: "
        f"{statement.period_start.isoformat()} to {statement.period_end.isoformat()}",
        f"Opening balance: {format_cents(statement.opening_balance_cents)}",
    ]
    for txn in statement.lines:
        out.append(
            f"{txn.posted_on.isoformat()}  "
            f"{format_cents(txn.amount_cents):>12}  {txn.description}"
        )
    out.append(f"Net change: {format_cents(statement.total_cents)}")
    out.append(f"Closing balance: {format_cents(statement.closing_balance_cents)}")
    return "\n".join(out)
