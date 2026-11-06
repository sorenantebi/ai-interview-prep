from formula.tokenizer import tokenize


def kinds(text):
    return [t.kind for t in tokenize(text)]


def test_simple_arithmetic_tokens():
    assert kinds("1 + 2") == ["NUMBER", "OP", "NUMBER", "END"]


def test_function_name_is_uppercased():
    toks = tokenize("sum(1, 2)")
    assert toks[0].kind == "FUNC"
    assert toks[0].value == "SUM"


def test_minus_between_operands_is_operator():
    assert kinds("5-3") == ["NUMBER", "OP", "NUMBER", "END"]


def test_negative_after_operator():
    toks = tokenize("3 * -2")
    assert [t.kind for t in toks] == ["NUMBER", "OP", "NUMBER", "END"]
    assert toks[2].value == -2.0
