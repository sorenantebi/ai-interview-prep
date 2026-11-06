from inventory.reports import low_stock, summary
from inventory.service import InventoryService


def make_service():
    svc = InventoryService()
    svc.add_product("a", "Alpha", on_hand=10)
    svc.add_product("b", "Bravo", on_hand=3)
    svc.add_product("c", "Charlie", on_hand=40)
    svc.add_product("d", "Delta", on_hand=5)
    svc.reserve("a", 9)
    return svc


def test_low_stock_includes_threshold_boundary():
    svc = make_service()
    skus = {p.sku for p in low_stock(svc, threshold=5)}
    assert skus == {"A", "B", "D"}


def test_low_stock_most_urgent_first():
    svc = make_service()
    skus = [p.sku for p in low_stock(svc, threshold=5)]
    assert skus == ["A", "B", "D"], f"got {skus}"


def test_summary_totals():
    svc = make_service()
    assert summary(svc) == {
        "products": 4,
        "on_hand": 58,
        "reserved": 9,
        "available": 49,
    }
