import time

from formula import EvalError, ParseError, Sheet, TokenError


def make_sheet():
    sheet = Sheet()
    sheet.set("A1", 10)
    sheet.set("B1", 4)
    return sheet


def expect(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    assert False, f"expected {exc.__name__}"


def test_mixed_chain():
    assert Sheet().evaluate("1 - 2 + 3") == 2


def test_long_subtraction_chain():
    assert Sheet().evaluate("100 - 10 - 20 - 30") == 40


def test_division_left_associative():
    assert Sheet().evaluate("8 / 4 / 2") == 1


def test_minus_negative_literal():
    assert Sheet().evaluate("5 - -3") == 8


def test_two_negative_factors():
    assert Sheet().evaluate("-2 * -3") == 6


def test_negative_in_middle_of_expression():
    assert Sheet().evaluate("2*-3+10") == 4


def test_negative_chain():
    assert Sheet().evaluate("-5 - -5 - 5") == -5


def test_negative_function_arguments():
    assert Sheet().evaluate("MAX(-1, -5)") == -1
    assert Sheet().evaluate("SUM(1, -2, -3.5)") == -4.5


def test_decimals_without_leading_zero():
    assert Sheet().evaluate("1.5 - .5 - .25") == 0.75


def test_subtraction_after_ref_and_paren_still_works():
    sheet = make_sheet()
    assert sheet.evaluate("A1-3") == 7
    assert sheet.evaluate("(5)-3") == 2


def test_mixed_case_function_and_refs():
    assert make_sheet().evaluate("sum(a1, B1)") == 14


def test_lowercase_reference_inside_formula_cell():
    sheet = make_sheet()
    sheet.set("C1", "=a1-b1-1")
    assert sheet.value("C1") == 5


def test_lowercase_circular_reference_detected():
    sheet = Sheet()
    sheet.set("A1", "=a1+1")
    expect(EvalError, sheet.value, "A1")


def test_lowercase_set_and_value():
    sheet = Sheet()
    sheet.set("a1", 7)
    assert sheet.value("A1") == 7
    assert sheet.value("a1") == 7


def test_nested_function_with_chain():
    assert make_sheet().evaluate("MAX(A1 - B1 - 3, -2)") == 3


def test_error_cases():
    expect(ParseError, Sheet().evaluate, "3 * ")
    expect(TokenError, Sheet().evaluate, "1 + #")
    expect(EvalError, Sheet().evaluate, "AVG()")


def test_long_formula_is_fast():
    formula = " - ".join(["1"] * 200)
    start = time.perf_counter()
    result = Sheet().evaluate(formula)
    assert result == 1 - 199
    assert time.perf_counter() - start < 1.0
