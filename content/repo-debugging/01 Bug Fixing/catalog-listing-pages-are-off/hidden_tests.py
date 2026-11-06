from catalog.models import Record
from catalog.repository import RecordRepository
from catalog.handlers import list_records
from catalog.pagination import offset_for, has_more, total_pages, paginate


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


def test_offset_values():
    assert offset_for(2, 5) == 5
    assert offset_for(1, 1) == 0
    assert offset_for(4, 25) == 75


def test_has_more_boundaries():
    assert has_more(10, 10, 20) is False
    assert has_more(10, 10, 21) is True
    assert has_more(0, 10, 10) is False
    assert has_more(0, 10, 11) is True


def test_single_exact_page():
    page = paginate(list(range(10)), 1, 10)
    assert len(page.items) == 10
    assert page.has_next is False


def test_page_size_one():
    items = ["a", "b", "c"]
    assert paginate(items, 1, 1).items == ["a"]
    assert paginate(items, 3, 1).items == ["c"]
    assert paginate(items, 3, 1).has_next is False
    assert paginate(items, 2, 1).has_next is True


def test_page_size_larger_than_total():
    page = paginate([1, 2, 3], 1, 10)
    assert page.items == [1, 2, 3]
    assert page.has_next is False


def test_empty_repository():
    status, body = list_records(make_repo(0), {})
    assert status == 200
    assert body["items"] == []
    assert body["total"] == 0
    assert body["total_pages"] == 0
    assert body["has_next"] is False


def test_walk_all_pages_without_gaps_or_duplicates():
    repo = make_repo(23)
    seen = []
    page = 1
    while True:
        status, body = list_records(repo, {"page": page, "page_size": 5})
        assert status == 200
        seen.extend(r["id"] for r in body["items"])
        if not body["has_next"]:
            break
        page += 1
        assert page <= 10, "has_next never became False"
    assert seen == list(range(1, 24))
    assert page == 5


def test_walk_exact_multiple():
    repo = make_repo(20)
    status, body = list_records(repo, {"page": 4, "page_size": 5})
    assert [r["id"] for r in body["items"]] == [16, 17, 18, 19, 20]
    assert body["has_next"] is False
    status, body = list_records(repo, {"page": 3, "page_size": 5})
    assert body["has_next"] is True


def test_zero_and_negative_params():
    assert list_records(make_repo(5), {"page": 0})[0] == 400
    assert list_records(make_repo(5), {"page": -2})[0] == 400
    assert list_records(make_repo(5), {"page_size": 0})[0] == 400
    assert list_records(make_repo(5), {"page_size": "x"})[0] == 400


def test_unknown_sort_key():
    status, body = list_records(make_repo(5), {"sort": "colour"})
    assert status == 400
    assert "colour" in body["error"]


def test_sort_by_price_across_pages():
    repo = make_repo(30)
    prices = []
    for page in (1, 2, 3):
        status, body = list_records(repo, {"sort": "price", "page": page, "page_size": 10})
        prices.extend(r["price_cents"] for r in body["items"])
    assert len(prices) == 30
    assert prices == sorted(prices)


def test_sort_by_name_and_id():
    repo = make_repo(12)
    _, body = list_records(repo, {"sort": "name", "page_size": 12})
    names = [r["name"] for r in body["items"]]
    assert names == sorted(names)
    _, body = list_records(repo, {"sort": "id", "page_size": 12})
    assert [r["id"] for r in body["items"]] == list(range(1, 13))


def test_category_with_pagination():
    repo = make_repo(30)
    status, body = list_records(repo, {"category": "tools", "page": 2, "page_size": 5})
    assert body["total"] == 10
    assert len(body["items"]) == 5
    assert body["has_next"] is False
    assert body["total_pages"] == 2


def test_unknown_category_is_empty():
    status, body = list_records(make_repo(10), {"category": "garden"})
    assert status == 200
    assert body["items"] == []
    assert body["total"] == 0


def test_total_pages_helper_exact():
    assert total_pages(50, 50) == 1
    assert total_pages(51, 50) == 2
