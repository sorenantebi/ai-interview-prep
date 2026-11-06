from cardgame.cards import Card, parse_card


def test_parse_number_cards_and_ace():
    assert parse_card("7H") == Card("7", "H")
    assert parse_card("7H").value == 7
    assert parse_card("10S").value == 10
    assert parse_card("AC").value == 1


def test_parse_normalises_case_and_whitespace():
    assert parse_card(" kd ") == Card("K", "D")
    assert str(parse_card("10d")) == "10D"


def test_face_cards_are_worth_ten():
    for text in ("JH", "QH", "KH", "JS", "QC", "KD"):
        assert parse_card(text).value == 10, f"{text} should be worth 10"


def test_parse_rejects_bad_input():
    for text in ("1H", "", "5X", "H"):
        try:
            parse_card(text)
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError for {text!r}")
