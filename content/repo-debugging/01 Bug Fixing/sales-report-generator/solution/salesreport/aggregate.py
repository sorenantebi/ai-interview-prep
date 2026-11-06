"""Grouping and totalling of sales."""

from salesreport.models import Sale


def region_key(name):
    """Normalise a region name so spelling variants map to one group."""
    return name.strip().upper()


def group_by_region(sales):
    """Return a dict mapping normalised region name to its list of sales."""
    groups = {}
    for sale in sales:
        groups.setdefault(region_key(sale.region), []).append(sale)
    return groups


def region_totals(sales):
    """Return a dict mapping normalised region name to the sum of amounts."""
    return {
        region: sum(sale.amount for sale in group)
        for region, group in group_by_region(sales).items()
    }


def rep_totals(sales):
    """Return a dict mapping rep name to the sum of that rep's amounts."""
    totals = {}
    for sale in sales:
        totals[sale.rep] = totals.get(sale.rep, 0.0) + sale.amount
    return totals
