"""Unit helpers for distances, speeds and travel times."""

KM_PER_MILE = 1.609344


def miles_to_km(miles):
    """Convert a distance in miles to kilometres."""
    return miles * KM_PER_MILE


def km_to_miles(km):
    """Convert a distance in kilometres to miles."""
    return km / KM_PER_MILE


def travel_minutes(distance_km, speed_kmh):
    """Minutes needed to cover ``distance_km`` at a constant ``speed_kmh``."""
    if speed_kmh <= 0:
        raise ValueError("speed must be positive")
    return distance_km / speed_kmh * 60.0
