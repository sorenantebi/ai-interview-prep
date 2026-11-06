"""Data model: transactions and accounts."""

from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass(frozen=True)
class Transaction:
    """A single posted entry. Deposits are positive, withdrawals negative."""

    posted_on: date
    amount_cents: int
    description: str = ""


@dataclass
class Account:
    """A customer account with an opening balance and a list of postings."""

    account_id: str
    annual_rate_bps: int = 0
    opening_balance_cents: int = 0
    transactions: List[Transaction] = field(default_factory=list)

    def post(self, transaction: Transaction) -> None:
        """Append a transaction to the account."""
        self.transactions.append(transaction)

    def balance_as_of(self, day: date) -> int:
        """Balance after all transactions posted on or before ``day``."""
        total = self.opening_balance_cents
        for txn in self.transactions:
            if txn.posted_on <= day:
                total += txn.amount_cents
        return total

    def transactions_between(self, start: date, end: date) -> List[Transaction]:
        """Transactions posted from ``start`` to ``end``, both inclusive,
        ordered by posting date (ties keep insertion order)."""
        selected = [t for t in self.transactions if start <= t.posted_on <= end]
        return sorted(selected, key=lambda t: t.posted_on)
