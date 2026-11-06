from formula import EvalError, Sheet


def make_sheet():
    sheet = Sheet()
    sheet.set("A1", 10)
    sheet.set("B1", 4)
    sheet.set("C1", "=A1-B1")
    return sheet


def test_formula_cell():
    assert make_sheet().value("C1") == 6


def test_functions():
    sheet = make_sheet()
    assert sheet.evaluate("SUM(A1, B1, 1)") == 15
    assert sheet.evaluate("MAX(A1, B1)") == 10
    assert sheet.evaluate("AVG(A1, B1)") == 7


def test_chained_subtraction():
    assert make_sheet().evaluate("A1 - B1 - 3") == 3


def test_negative_literals():
    sheet = make_sheet()
    assert sheet.evaluate("B1 * -2") == -8
    assert sheet.evaluate("-2 * 3") == -6


def test_lowercase_reference():
    assert make_sheet().evaluate("a1 + b1") == 14


def test_division_by_zero():
    try:
        make_sheet().evaluate("A1 / 0")
    except EvalError:
        return
    assert False, "expected EvalError"
