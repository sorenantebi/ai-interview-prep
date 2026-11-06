from catalog.pagination import offset_for, has_more, total_pages, paginate


def numbers(n):
    return list(range(1, n + 1))


def test_offset_first_page():
    assert offset_for(1, 10) == 0, "page 1 should start at index 0"


def test_offset_later_page():
    assert offset_for(3, 10) == 20


def test_total_pages():
    assert total_pages(0, 10) == 0
    assert total_pages(1, 10) == 1
    assert total_pages(10, 10) == 1
    assert total_pages(11, 10) == 2


def test_first_page_items():
    page = paginate(numbers(25), 1, 10)
    assert page.items == list(range(1, 11))
    assert page.total == 25


def test_middle_page():
    page = paginate(numbers(25), 2, 10)
    assert page.items == list(range(11, 21))
    assert page.has_next is True


def test_last_partial_page():
    page = paginate(numbers(25), 3, 10)
    assert page.items == list(range(21, 26))
    assert page.has_next is False


def test_last_full_page_has_no_next():
    page = paginate(numbers(20), 2, 10)
    assert page.items == list(range(11, 21))
    assert page.has_next is False


def test_page_past_the_end():
    page = paginate(numbers(25), 9, 10)
    assert page.items == []
    assert page.has_next is False


def test_has_more_helper():
    assert has_more(0, 10, 11) is True
