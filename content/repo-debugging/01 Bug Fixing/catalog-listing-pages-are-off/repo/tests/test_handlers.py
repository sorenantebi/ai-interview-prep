from catalog.models import Record
from catalog.repository import RecordRepository
from catalog.handlers import list_records


def make_repo(n):
    repo = RecordRepository()
    for i in range(1, n + 1):
        repo.add(Record(
            id=i,
            name=f"Item {i:03d}",
            category="tools" if i % 3 == 0 else "toys",
            price_cents=100 + (i * 37 % 97) * 10,
        ))
    return repo


def test_default_listing():
    status, body = list_records(make_repo(25), {})
    assert status == 200
    assert [r["id"] for r in body["items"]] == list(range(1, 11))
    assert body["total"] == 25
    assert body["total_pages"] == 3
    assert body["has_next"] is True


def test_string_params_are_accepted():
    status, body = list_records(make_repo(25), {"page": "2", "page_size": "5"})
    assert status == 200
    assert [r["id"] for r in body["items"]] == [6, 7, 8, 9, 10]


def test_invalid_page_is_rejected():
    status, body = list_records(make_repo(5), {"page": "abc"})
    assert status == 400
    assert "page" in body["error"]


def test_page_size_is_capped():
    status, body = list_records(make_repo(80), {"page_size": 500})
    assert status == 200
    assert body["page_size"] == 50
    assert len(body["items"]) == 50


def test_category_filter():
    status, body = list_records(make_repo(30), {"category": "tools"})
    assert status == 200
    assert body["total"] == 10
    assert all(r["category"] == "tools" for r in body["items"])


def test_sort_by_price():
    status, body = list_records(make_repo(30), {"sort": "price", "page_size": 30})
    prices = [r["price_cents"] for r in body["items"]]
    assert prices == sorted(prices)


def test_last_full_page_via_handler():
    status, body = list_records(make_repo(20), {"page": 2})
    assert len(body["items"]) == 10
    assert body["has_next"] is False
