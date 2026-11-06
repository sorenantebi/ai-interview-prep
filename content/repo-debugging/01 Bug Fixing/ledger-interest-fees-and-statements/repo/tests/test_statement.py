from datetime import date

from ledger.models import Account, Transaction
from ledger.statement import build_statement, render_statement


def make_account():
    acct = Account("A-7", annual_rate_bps=100, opening_balance_cents=50_000)
    acct.post(Transaction(date(2025, 3, 31), 7_000, "march deposit"))
    acct.post(Transaction(date(2025, 4, 3), 100_000, "salary"))
    acct.post(Transaction(date(2025, 4, 10), -2_500, "groceries"))
    acct.post(Transaction(date(2025, 4, 20), -1_000, "phone"))
    acct.post(Transaction(date(2025, 5, 1), -9_999, "may rent"))
    return acct


def test_statement_lists_only_transactions_in_month():
    stmt = build_statement(make_account(), 2025, 4)
    assert [t.description for t in stmt.lines] == ["salary", "groceries", "phone"]


def test_statement_opening_balance():
    stmt = build_statement(make_account(), 2025, 4)
    assert stmt.opening_balance_cents == 57_000


def test_statement_total():
    stmt = build_statement(make_account(), 2025, 4)
    assert stmt.total_cents == 96_500, "net change should include every line"


def test_statement_closing_balance():
    stmt = build_statement(make_account(), 2025, 4)
    assert stmt.closing_balance_cents == 153_500


def test_single_transaction_statement():
    acct = Account("A-8")
    acct.post(Transaction(date(2025, 6, 15), 5_000, "gift"))
    assert build_statement(acct, 2025, 6).total_cents == 5_000


def test_render_statement_shows_net_change():
    text = render_statement(build_statement(make_account(), 2025, 4))
    assert "Net change: $965.00" in text
    assert "Closing balance: $1,535.00" in text
