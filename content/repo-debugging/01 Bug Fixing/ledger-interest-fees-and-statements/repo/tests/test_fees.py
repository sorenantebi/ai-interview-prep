from ledger.fees import overdraft_fee_cents, wire_fee_cents


def test_wire_fee_minimum():
    assert wire_fee_cents(10_000) == 100


def test_wire_fee_regular_amount():
    assert wire_fee_cents(100_000) == 500


def test_wire_fee_cap():
    assert wire_fee_cents(10_000_000) == 2_500


def test_wire_fee_half_cent_rounds_up():
    # 0.5% of $301.00 is $1.505, which rounds to $1.51
    assert wire_fee_cents(30_100) == 151, "expected 151 cents"


def test_wire_fee_rejects_non_positive_amounts():
    try:
        wire_fee_cents(0)
    except ValueError:
        return
    assert False, "expected ValueError"


def test_overdraft_fee():
    assert overdraft_fee_cents(-1) == 3_500
    assert overdraft_fee_cents(0) == 0
    assert overdraft_fee_cents(12_345) == 0
