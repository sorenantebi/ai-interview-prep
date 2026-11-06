from datetime import datetime, timedelta
from decimal import Decimal

from parking.models import VehicleType
from parking.pricing import calculate_fee

T0 = datetime(2025, 3, 3, 8, 0)


def test_zero_duration_is_free():
    assert calculate_fee(T0, T0) == Decimal("0")


def test_partial_hour_rounds_up_at_flat_rate():
    fee = calculate_fee(T0, T0 + timedelta(minutes=61))
    assert fee == Decimal("4.00")


def test_car_pays_its_hourly_rate():
    fee = calculate_fee(T0, T0 + timedelta(hours=3), VehicleType.CAR)
    assert fee == Decimal("7.50")


def test_car_daily_cap():
    fee = calculate_fee(T0, T0 + timedelta(hours=8), VehicleType.CAR)
    assert fee == Decimal("15.00"), "8h x 2.50 exceeds the 15.00 cap"


def test_caps_differ_per_vehicle_type():
    stay = timedelta(hours=10)
    assert calculate_fee(T0, T0 + stay, VehicleType.MOTORCYCLE) == Decimal("6.00")
    assert calculate_fee(T0, T0 + stay, VehicleType.VAN) == Decimal("24.00")
