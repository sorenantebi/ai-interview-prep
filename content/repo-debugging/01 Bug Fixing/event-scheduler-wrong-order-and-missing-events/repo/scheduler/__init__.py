"""Small event scheduler used by the team calendar."""

from scheduler.models import Event
from scheduler.service import Scheduler

__all__ = ["Event", "Scheduler"]
