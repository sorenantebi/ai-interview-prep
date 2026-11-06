from datetime import date

from ledger.fees import overdraft_fee_cents, wire_fee_cents
from ledger.interest import accrue_monthly, interest_for_period
from ledger.models import Account, Transaction
from ledger.money import div_round_half_up, format_cents
from ledger.statement import build_statement, net_total_cents, render_statement


def test_interest_half_cent_rounds_up():
    assert interest_for_period(365_000, 25, 1) == 3


def test_interest_thirty_one_days():
    assert interest_for_period(1_000_000, 450, 31) == 3822


def test_interest_full_year_is_exact():
    assert interest_for_period(1_000_000, 500, 365) == 50_000


def test_interest_zero_rate():
    assert interest_for_period(1_000_000, 0, 30) == 0


def test_interest_returns_int():
    assert isinstance(interest_for_period(123_456, 321, 17), int)


def test_accrue_monthly_leap_february():
    acct = Account("H-1", annual_rate_bps=300, opening_balance_cents=2_000_000)
    assert accrue_monthly(acct, 2024, 2) == 4767


def test_accrue_monthly_ignores_mid_month_deposit():
    acct = Account("H-2", annual_rate_bps=450, opening_balance_cents=1_000_000)
    acct.post(Transaction(date(2025, 4, 1), 5_000_000, "big deposit"))
    assert accrue_monthly(acct, 2025, 4) == 3699


def test_wire_fee_other_half_cents():
    assert wire_fee_cents(30_500) == 153
    assert wire_fee_cents(30_700) == 154


def test_wire_fee_boundaries():
    assert wire_fee_cents(20_000) == 100
    assert wire_fee_cents(19_999) == 100
    assert wire_fee_cents(500_000) == 2_500
    assert wire_fee_cents(500_100) == 2_500


def test_wire_fee_is_int():
    assert isinstance(wire_fee_cents(123_457), int)


def test_overdraft_boundaries():
    assert overdraft_fee_cents(0) == 0
    assert overdraft_fee_cents(-1) == 3_500


def test_statement_empty_month():
    acct = Account("H-3", opening_balance_cents=10_000)
    acct.post(Transaction(date(2025, 1, 5), 500, "jan"))
    stmt = build_statement(acct, 2025, 2)
    assert stmt.lines == []
    assert stmt.total_cents == 0
    assert stmt.closing_balance_cents == 10_500


def test_statement_sorted_and_negative_total():
    acct = Account("H-4")
    acct.post(Transaction(date(2025, 7, 20), -3_000, "c"))
    acct.post(Transaction(date(2025, 7, 2), -1_000, "a"))
    acct.post(Transaction(date(2025, 7, 11), 500, "b"))
    stmt = build_statement(acct, 2025, 7)
    assert [t.description for t in stmt.lines] == ["a", "b", "c"]
    assert stmt.total_cents == -3_500
    assert stmt.closing_balance_cents == -3_500


def test_statement_month_boundaries_and_december():
    acct = Account("H-5")
    acct.post(Transaction(date(2024, 12, 1), 100, "first"))
    acct.post(Transaction(date(2024, 12, 31), 200, "last"))
    acct.post(Transaction(date(2025, 1, 1), 400, "next year"))
    stmt = build_statement(acct, 2024, 12)
    assert stmt.period_end == date(2024, 12, 31)
    assert stmt.total_cents == 300


def test_statement_same_day_transactions():
    acct = Account("H-6")
    acct.post(Transaction(date(2025, 9, 9), 1_000, "x"))
    acct.post(Transaction(date(2025, 9, 9), -400, "y"))
    assert build_statement(acct, 2025, 9).total_cents == 600


def test_net_total_helper():
    txns = [Transaction(date(2025, 1, d), d * 10) for d in range(1, 5)]
    assert net_total_cents(txns) == 100
    assert net_total_cents([]) == 0


def test_render_negative_amounts():
    acct = Account("H-7", opening_balance_cents=1_000)
    acct.post(Transaction(date(2025, 2, 3), -2_550, "rent"))
    text = render_statement(build_statement(acct, 2025, 2))
    assert "Net change: -$25.50" in text
    assert "Closing balance: -$15.50" in text


def test_money_helpers():
    assert div_round_half_up(5, 2) == 3
    assert div_round_half_up(-5, 2) == -3
    assert div_round_half_up(1, 3) == 0
    assert format_cents(123_456_789) == "$1,234,567.89"
    assert format_cents(-5) == "-$0.05"
