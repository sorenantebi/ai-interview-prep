from datetime import datetime, timedelta
from decimal import Decimal

from parking.models import Receipt, Ticket, VehicleType
from parking.reports import revenue_by_type

T0 = datetime(2025, 3, 3, 8, 0)


def _receipt(ticket_id, vehicle_type, fee):
    ticket = Ticket(ticket_id, f"P-{ticket_id}", vehicle_type, "X1", T0)
    return Receipt(ticket, T0 + timedelta(hours=1), Decimal(fee))


def test_revenue_by_type_sums_per_vehicle_type():
    receipts = [
        _receipt(1, VehicleType.CAR, "4.00"),
        _receipt(2, VehicleType.CAR, "6.00"),
        _receipt(3, VehicleType.VAN, "8.00"),
    ]
    totals = revenue_by_type(receipts)
    assert totals == {"car": Decimal("10.00"), "van": Decimal("8.00")}
