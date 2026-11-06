---
difficulty: Medium
kind: extend
---
# EV charging spots and capped hourly pricing

**Kind:** Extend the codebase · **Difficulty:** Medium

## Scenario
The `parking` package manages a small car park: it hands out spots to arriving vehicles, issues tickets and computes the fee when a vehicle leaves. Operators are installing EV chargers and want the system to reserve those spots for vehicles that need charging. At the same time, the flat 2.00-per-hour fee is being replaced by per-vehicle-type hourly rates with a daily cap. The existing behaviour is covered by passing tests; the tests for the new features fail until you build them.

## Your tasks
1. **EV charging spots.**
   - Add a new spot type `SpotType.EV` (value `"ev"`). Spot ids for it use the prefix `E` (`E1`, `E2`, ...).
   - `Vehicle` gets a new optional field `needs_charging` (default `False`).
   - A vehicle with `needs_charging=True` may only be parked in an EV spot, whatever its vehicle type. If none is free, parking raises `LotFullError`.
   - Vehicles that do not need charging must never be given an EV spot.
   - `ParkingLot.available()` must report the free EV spots under the key `"ev"`.
2. **Hourly pricing with a daily cap per vehicle type.**
   - `calculate_fee(entry_time, exit_time, vehicle_type=None)` accepts an optional third argument. Without it, the behaviour stays exactly as it is today (flat 2.00 per started hour).
   - With a vehicle type, each started hour costs the type's hourly rate, but the price of any 24-hour block is capped. Every complete 24 hours cost exactly the daily cap, and the remaining started hours cost `min(hours * rate, cap)`.

     | Vehicle type | Hourly rate | Daily cap |
     |--------------|-------------|-----------|
     | motorcycle   | 1.00        | 6.00      |
     | car          | 2.50        | 15.00     |
     | van          | 4.00        | 24.00     |

   - `ParkingLot.leave` must charge the fee of the vehicle type on the ticket.
   - Fees are `Decimal` values.

## Notes
- Entry points: `parking/lot.py` (`ParkingLot.park` / `leave` / `available`), `parking/pricing.py` (`calculate_fee`) and `parking/allocator.py` (which spot types a vehicle may use).
- Keep the existing tests green. Follow the existing structure instead of adding parallel code paths.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
