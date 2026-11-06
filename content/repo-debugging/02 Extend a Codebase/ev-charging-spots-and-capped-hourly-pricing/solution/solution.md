# EV charging spots and capped hourly pricing - Solution

## Root causes / approach
This is a feature task. The design extends the existing seams instead of adding new code paths.

**EV charging spots** (`models.py`, `allocator.py`, `lot.py`)
- `models.py`: add `SpotType.EV = "ev"` and a defaulted field `needs_charging: bool = False` on the frozen `Vehicle` dataclass. The default keeps every existing call site valid.
- `lot.py`: add `SpotType.EV: "E"` to `SPOT_PREFIX`. Without it, building a layout with EV spots raises `KeyError`. `available()` already iterates over `SpotType`, so the `"ev"` key appears with no further change.
- `allocator.py`: `preferred_spot_types` is the single place that decides which spot types a vehicle may use. A charging vehicle gets `(SpotType.EV,)`, so it never falls back to a compact spot and fails with `LotFullError` when no EV spot is free. Vehicles that do not charge keep their existing preference tuples, which do not contain `EV`, so they never take an EV spot. `find_spot` needs no change.

**Pricing** (`pricing.py`, `lot.py`)
- Add a `Tariff` dataclass (hourly rate, daily cap) and a `TARIFFS` table keyed by `VehicleType`.
- `calculate_fee` gets an optional `vehicle_type`. With `None` it returns the old flat result, so existing callers and tests are unaffected.
- With a type, it computes `started_hours`, then `full_days, rest = divmod(hours, 24)`. The fee is `daily_cap * full_days + min(hourly_rate * rest, daily_cap)`. Doing this in integer hours with `Decimal` rates avoids float rounding and handles exact multiples of 24 hours (exactly 24h is one cap, not a cap plus 0).
- `ParkingLot.leave` now passes `ticket.vehicle_type`. The `Ticket` already carries the vehicle type, so no new state is needed.
- `reports.revenue_by_type` and `utils.py` needed no changes.

Complexity is O(1) for the fee and unchanged for allocation (O(spots)).

## How to find it
- Run the tests and read the first failures. `test_charging_vehicle_gets_ev_spot` fails with `AttributeError: EV`, which points to the `SpotType` enum, then to `SPOT_PREFIX` and `Vehicle`.
- `test_car_pays_its_hourly_rate` fails with a `TypeError` about an unexpected third argument. That points to `calculate_fee` in `pricing.py`. Its callers are found by searching for it, and `ParkingLot.leave` is the only one.
- Before changing `allocator.py`, read `find_spot` and `_PREFERENCES` to see that preferences are the one place that controls which spot types are allowed.
- After implementing, check the boundaries by hand: 24h, 25h and 48h for a car (15.00, 17.50, 30.00), and a 61-minute stay (two started hours).
