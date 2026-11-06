from inventory.errors import (
    InsufficientStockError,
    ReservationNotFoundError,
    UnknownProductError,
)
from inventory.service import InventoryService


def make_service():
    svc = InventoryService()
    svc.add_product("abc-1", "Widget", on_hand=10)
    svc.add_product("xyz-9", "Gadget", on_hand=2)
    return svc


def test_add_and_get_normalizes_sku():
    svc = make_service()
    assert svc.get("  abc-1 ").name == "Widget"
    assert svc.get("ABC-1").sku == "ABC-1"


def test_unknown_product():
    svc = make_service()
    try:
        svc.get("nope")
    except UnknownProductError:
        return
    assert False, "expected UnknownProductError"


def test_reserve_reduces_available():
    svc = make_service()
    res = svc.reserve("abc-1", 4)
    assert res.quantity == 4
    assert svc.available("abc-1") == 6


def test_reserve_more_than_available_raises():
    svc = make_service()
    svc.reserve("xyz-9", 1)
    try:
        svc.reserve("xyz-9", 5)
    except InsufficientStockError:
        return
    assert False, "expected InsufficientStockError"


def test_reserve_exact_remaining_succeeds():
    svc = make_service()
    svc.reserve("xyz-9", 2)
    assert svc.available("xyz-9") == 0


def test_reserve_when_nothing_left_raises():
    svc = make_service()
    svc.reserve("xyz-9", 2)
    try:
        svc.reserve("xyz-9", 1)
    except InsufficientStockError:
        return
    assert False, "reserving with zero units left must fail"


def test_release_returns_stock():
    svc = make_service()
    res = svc.reserve("abc-1", 3)
    svc.release(res.id)
    assert svc.available("abc-1") == 10
    try:
        svc.release(res.id)
    except ReservationNotFoundError:
        return
    assert False, "second release should fail"


def test_commit_ships_units():
    svc = make_service()
    res = svc.reserve("abc-1", 4)
    svc.commit(res.id)
    product = svc.get("abc-1")
    assert product.on_hand == 6
    assert product.reserved == 0


def test_restock_adds_units():
    svc = make_service()
    svc.restock("abc-1", 5)
    assert svc.get("abc-1").on_hand == 15
    assert svc.available("abc-1") == 15


def test_restock_keeps_reserved_units():
    svc = make_service()
    svc.reserve("abc-1", 4)
    svc.restock("abc-1", 5)
    product = svc.get("abc-1")
    assert product.reserved == 4, "open reservations must survive a restock"
    assert product.on_hand == 15
    assert product.available == 11


def test_invalid_quantities_rejected():
    svc = make_service()
    for bad in (0, -3, 1.5):
        try:
            svc.reserve("abc-1", bad)
        except ValueError:
            continue
        assert False, f"quantity {bad!r} should be rejected"
