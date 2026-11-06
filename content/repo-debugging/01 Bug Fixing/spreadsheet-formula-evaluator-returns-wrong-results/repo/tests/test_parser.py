from formula.errors import ParseError
from formula.parser import BinOp, Call, Number, Ref, parse


def test_precedence():
    expected = BinOp("+", Number(1.0), BinOp("*", Number(2.0), Number(3.0)))
    assert parse("1 + 2 * 3") == expected


def test_function_call():
    assert parse("SUM(A1, 2)") == Call("SUM", (Ref("A1"), Number(2.0)))


def test_subtraction_is_left_associative():
    expected = BinOp("-", BinOp("-", Number(10.0), Number(4.0)), Number(3.0))
    assert parse("10 - 4 - 3") == expected


def test_missing_closing_paren():
    try:
        parse("(1 + 2")
    except ParseError:
        return
    assert False, "expected ParseError"
