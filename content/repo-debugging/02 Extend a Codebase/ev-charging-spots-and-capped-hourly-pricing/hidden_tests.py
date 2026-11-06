from datetime import datetime, timedelta
from decimal import Decimal

from parking.lot import LotFullError, ParkingLot
from parking.models import SpotType, Vehicle, VehicleType
from parking.pricing import calculate_fee

T0 = datetime(2025, 3, 3, 8, 0)


def _fee(hours, vehicle_type, extra_minutes=0):
    stay = timedelta(hours=hours, minutes=extra_minutes)
    return calculate_fee(T0, T0 + stay, vehicle_type)


def test_flat_rate_without_vehicle_type_has_no_cap():
    assert calculate_fee(T0, T0 + timedelta(hours=30)) == Decimal("60.00")


def test_typed_fee_zero_and_negative_durations():
    assert calculate_fee(T0, T0, VehicleType.CAR) == Decimal("0")
    assert calculate_fee(T0, T0 - timedelta(hours=2), VehicleType.VAN) == Decimal("0")


def test_partial_hour_rounds_up_with_tariff():
    assert _fee(1, VehicleType.CAR, extra_minutes=1) == Decimal("5.00")


def test_exact_cap_boundary():
    assert _fee(6, VehicleType.CAR) == Decimal("15.00")
    assert _fee(5, VehicleType.CAR) == Decimal("12.50")


def test_exactly_24_hours_costs_one_cap():
    assert _fee(24, VehicleType.CAR) == Decimal("15.00")
    assert _fee(24, VehicleType.MOTORCYCLE) == Decimal("6.00")


def test_just_over_24_hours_starts_new_block():
    assert _fee(25, VehicleType.CAR) == Decimal("17.50")
    assert _fee(24, VehicleType.VAN, extra_minutes=30) == Decimal("28.00")


def test_multiple_days():
    assert _fee(48, VehicleType.CAR) == Decimal("30.00")
    assert _fee(30, VehicleType.VAN) == Decimal("48.00")
    assert _fee(26, VehicleType.CAR) == Decimal("20.00")


def test_van_and_motorcycle_below_cap():
    assert _fee(5, VehicleType.VAN) == Decimal("20.00")
    assert _fee(5, VehicleType.MOTORCYCLE) == Decimal("5.00")


def test_vehicle_defaults_to_not_charging():
    assert Vehicle("A-1", VehicleType.CAR).needs_charging is False


def test_ev_spot_ids_and_exhaustion():
    lot = ParkingLot({SpotType.EV: 2, SpotType.COMPACT: 3})
    first = lot.park(Vehicle("E-1", VehicleType.CAR, needs_charging=True), T0)
    second = lot.park(Vehicle("E-2", VehicleType.CAR, needs_charging=True), T0)
    assert (first.spot_id, second.spot_id) == ("E1", "E2")
    try:
        lot.park(Vehicle("E-3", VehicleType.CAR, needs_charging=True), T0)
    except LotFullError:
        pass
    else:
        assert False, "third charging vehicle must not get a compact spot"
    assert lot.available()["compact"] == 3


def test_charging_motorcycle_uses_ev_spot():
    lot = ParkingLot({SpotType.MOTORCYCLE: 1, SpotType.EV: 1})
    ticket = lot.park(Vehicle("M-1", VehicleType.MOTORCYCLE, needs_charging=True), T0)
    assert ticket.spot_id == "E1"


def test_ev_spot_is_reused_after_leaving():
    lot = ParkingLot({SpotType.EV: 1})
    ticket = lot.park(Vehicle("E-1", VehicleType.CAR, needs_charging=True), T0)
    lot.leave(ticket.ticket_id, T0 + timedelta(hours=1))
    assert lot.available()["ev"] == 1
    again = lot.park(Vehicle("E-2", VehicleType.CAR, needs_charging=True), T0)
    assert again.spot_id == "E1"


def test_available_has_ev_key_even_without_ev_spots():
    lot = ParkingLot({SpotType.COMPACT: 1})
    assert lot.available()["ev"] == 0


def test_charging_car_pays_car_tariff():
    lot = ParkingLot({SpotType.EV: 1})
    ticket = lot.park(Vehicle("E-1", VehicleType.CAR, needs_charging=True), T0)
    receipt = lot.leave(ticket.ticket_id, T0 + timedelta(hours=26))
    assert receipt.fee == Decimal("20.00")


def test_motorcycle_falls_back_to_compact():
    lot = ParkingLot({SpotType.COMPACT: 1, SpotType.LARGE: 1})
    ticket = lot.park(Vehicle("M-1", VehicleType.MOTORCYCLE), T0)
    assert ticket.spot_id == "C1"


def test_duplicate_plate_rejected():
    lot = ParkingLot({SpotType.COMPACT: 2})
    lot.park(Vehicle("CAR-1", VehicleType.CAR), T0)
    try:
        lot.park(Vehicle("CAR-1", VehicleType.CAR), T0)
    except ValueError:
        return
    assert False, "same plate parked twice"


def test_unknown_ticket_raises_key_error():
    lot = ParkingLot({SpotType.COMPACT: 1})
    try:
        lot.leave(99, T0)
    except KeyError:
        return
    assert False, "expected KeyError"
