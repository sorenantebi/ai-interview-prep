"""Parsing of partner road feeds."""

import csv
import io

_TRUE_VALUES = {"1", "true", "yes", "y"}


def _flag(value):
    return (value or "").strip().lower() in _TRUE_VALUES


def parse_roads(text):
    """Parse CSV text into a list of road rows.

    Expected header: ``origin,destination,distance,unit,speed_kmh,one_way,closed``.
    ``unit``, ``one_way`` and ``closed`` may be empty; the unit then defaults
    to kilometres.
    """
    rows = []
    reader = csv.DictReader(io.StringIO(text.strip()))
    for line in reader:
        rows.append(
            {
                "origin": line["origin"].strip(),
                "destination": line["destination"].strip(),
                "distance": float(line["distance"]),
                "unit": (line.get("unit") or "km").strip().lower(),
                "speed_kmh": float(line["speed_kmh"]),
                "one_way": _flag(line.get("one_way")),
                "closed": _flag(line.get("closed")),
            }
        )
    return rows
