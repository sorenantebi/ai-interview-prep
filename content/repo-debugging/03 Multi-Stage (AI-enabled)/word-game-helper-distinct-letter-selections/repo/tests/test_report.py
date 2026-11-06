from wordgame.report import format_summary, summarize_text


def test_summarize_empty_text():
    assert summarize_text("") == {"words": 0, "usable": 0, "best_length": 0}


def test_summarize_mixed_list():
    summary = summarize_text("cha r act ers hello")
    assert summary == {"words": 5, "usable": 4, "best_length": 6}


def test_format_summary():
    text = format_summary({"words": 5, "usable": 4, "best_length": 6})
    assert text == "4 of 5 words usable, best total length 6"
