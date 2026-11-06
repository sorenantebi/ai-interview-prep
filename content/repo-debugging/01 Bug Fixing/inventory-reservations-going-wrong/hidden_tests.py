from inventory.errors import (
    InsufficientStockError,
    ReservationNotFoundError,
    UnknownProductError,
)
from inventory.reports import low_stock, summary
from inventory.service import InventoryService


def make_service():
    svc = InventoryService()
    svc.add_product("a", "Alpha", on_hand=10)
    svc.add_product("b", "Bravo", on_hand=3)
    svc.add_product("c", "Charlie", on_hand=0)
    return svc


def raises(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return True
    return False


def test_reserve_on_empty_product_fails():
    svc = make_service()
    assert raises(InsufficientStockError, svc.reserve, "c", 1)


def test_failed_reserve_leaves_state_unchanged():
    svc = make_service()
    svc.reserve("b", 3)
    assert raises(InsufficientStockError, svc.reserve, "b", 1)
    assert svc.get("b").reserved == 3
    assert raises(ReservationNotFoundError, svc.release, 2)


def test_reserve_with_unnormalized_sku_when_empty():
    svc = make_service()
    svc.reserve(" B ", 3)
    assert raises(InsufficientStockError, svc.reserve, "b", 2)


def test_reserve_unknown_sku():
    svc = make_service()
    assert raises(UnknownProductError, svc.reserve, "zzz", 1)


def test_restock_after_sellout_then_reserve():
    svc = make_service()
    svc.reserve("b", 3)
    svc.restock("b", 4)
    product = svc.get("b")
    assert (product.on_hand, product.reserved, product.available) == (7, 3, 4)
    svc.reserve("b", 4)
    assert raises(InsufficientStockError, svc.reserve, "b", 1)


def test_restock_twice_accumulates():
    svc = make_service()
    svc.reserve("a", 2)
    svc.restock("a", 1)
    svc.restock("a", 1)
    product = svc.get("a")
    assert product.on_hand == 12
    assert product.reserved == 2


def test_restock_then_release_restores_correctly():
    svc = make_service()
    res = svc.reserve("a", 5)
    svc.restock("a", 5)
    svc.release(res.id)
    product = svc.get("a")
    assert product.reserved == 0
    assert product.available == 15


def test_restock_then_commit():
    svc = make_service()
    res = svc.reserve("a", 5)
    svc.restock("a", 5)
    svc.commit(res.id)
    product = svc.get("a")
    assert (product.on_hand, product.reserved) == (10, 0)


def test_restock_invalid_and_unknown():
    svc = make_service()
    assert raises(ValueError, svc.restock, "a", 0)
    assert raises(UnknownProductError, svc.restock, "zzz", 1)


def test_commit_twice_fails():
    svc = make_service()
    res = svc.reserve("a", 1)
    svc.commit(res.id)
    assert raises(ReservationNotFoundError, svc.commit, res.id)


def test_products_sorted_by_sku():
    svc = make_service()
    assert [p.sku for p in svc.products()] == ["A", "B", "C"]


def test_low_stock_threshold_zero_only_sold_out():
    svc = make_service()
    svc.reserve("b", 3)
    skus = [p.sku for p in low_stock(svc, threshold=0)]
    assert skus == ["B", "C"]


def test_low_stock_orders_by_available_not_on_hand():
    svc = InventoryService()
    svc.add_product("big", "Big", on_hand=100)
    svc.add_product("small", "Small", on_hand=4)
    svc.reserve("big", 98)
    skus = [p.sku for p in low_stock(svc, threshold=10)]
    assert skus == ["BIG", "SMALL"]


def test_low_stock_ties_broken_by_sku():
    svc = InventoryService()
    svc.add_product("m", "M", on_hand=2)
    svc.add_product("k", "K", on_hand=2)
    svc.add_product("z", "Z", on_hand=9)
    svc.reserve("z", 7)
    skus = [p.sku for p in low_stock(svc, threshold=2)]
    assert skus == ["K", "M", "Z"]


def test_low_stock_excludes_well_stocked():
    svc = make_service()
    skus = [p.sku for p in low_stock(svc, threshold=3)]
    assert "A" not in skus


def test_summary_after_restock_and_commit():
    svc = make_service()
    res = svc.reserve("a", 4)
    svc.restock("b", 2)
    svc.commit(res.id)
    assert summary(svc) == {
        "products": 3,
        "on_hand": 11,
        "reserved": 0,
        "available": 11,
    }
