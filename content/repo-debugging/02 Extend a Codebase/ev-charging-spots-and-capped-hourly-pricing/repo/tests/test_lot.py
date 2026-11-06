from datetime import datetime, timedelta
from decimal import Decimal

from parking.lot import LotFullError, ParkingLot
from parking.models import SpotType, Vehicle, VehicleType

T0 = datetime(2025, 3, 3, 8, 0)


def test_car_gets_smallest_fitting_spot():
    lot = ParkingLot({SpotType.REGULAR: 1, SpotType.COMPACT: 1})
    ticket = lot.park(Vehicle("CAR-1", VehicleType.CAR), T0)
    assert ticket.spot_id == "C1"


def test_van_goes_to_large_spot():
    lot = ParkingLot({SpotType.COMPACT: 2, SpotType.LARGE: 1})
    ticket = lot.park(Vehicle("VAN-1", VehicleType.VAN), T0)
    assert ticket.spot_id == "L1"


def test_lot_full_raises():
    lot = ParkingLot({SpotType.COMPACT: 1})
    lot.park(Vehicle("CAR-1", VehicleType.CAR), T0)
    try:
        lot.park(Vehicle("CAR-2", VehicleType.CAR), T0)
    except LotFullError:
        return
    assert False, "expected LotFullError"


def test_leave_frees_the_spot():
    lot = ParkingLot({SpotType.COMPACT: 1})
    ticket = lot.park(Vehicle("CAR-1", VehicleType.CAR), T0)
    assert lot.available()["compact"] == 0
    lot.leave(ticket.ticket_id, T0 + timedelta(hours=1))
    assert lot.available()["compact"] == 1


def test_charging_vehicle_gets_ev_spot():
    lot = ParkingLot({SpotType.COMPACT: 1, SpotType.EV: 1})
    vehicle = Vehicle("EV-1", VehicleType.CAR, needs_charging=True)
    ticket = lot.park(vehicle, T0)
    assert ticket.spot_id == "E1"
    assert lot.available()["ev"] == 0


def test_regular_car_never_takes_ev_spot():
    lot = ParkingLot({SpotType.EV: 1})
    try:
        lot.park(Vehicle("CAR-1", VehicleType.CAR), T0)
    except LotFullError:
        return
    assert False, "EV spots are reserved for charging vehicles"


def test_charging_vehicle_needs_an_ev_spot():
    lot = ParkingLot({SpotType.COMPACT: 2})
    vehicle = Vehicle("EV-1", VehicleType.CAR, needs_charging=True)
    try:
        lot.park(vehicle, T0)
    except LotFullError:
        return
    assert False, "no EV spot exists, so parking must fail"


def test_leave_charges_the_vehicle_tariff():
    lot = ParkingLot({SpotType.LARGE: 1})
    ticket = lot.park(Vehicle("VAN-1", VehicleType.VAN), T0)
    receipt = lot.leave(ticket.ticket_id, T0 + timedelta(hours=2))
    assert receipt.fee == Decimal("8.00")
