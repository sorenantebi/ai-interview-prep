from salesreport.aggregate import group_by_region, region_totals, rep_totals
from salesreport.parser import parse_sales

CSV = (
    "region,rep,amount\n"
    "EU,Alice,100.50\n"
    "eu,Bob,50.25\n"
    "US,Carol,300.00\n"
    "us,Alice,25.00\n"
)


def test_group_by_region_merges_spelling_variants():
    groups = group_by_region(parse_sales(CSV))
    assert sorted(groups) == ["EU", "US"], "regions should be merged regardless of case"
    assert len(groups["EU"]) == 2


def test_region_totals():
    totals = region_totals(parse_sales(CSV))
    assert totals == {"EU": 150.75, "US": 325.0}


def test_rep_totals():
    totals = rep_totals(parse_sales(CSV))
    assert totals == {"Alice": 125.5, "Bob": 50.25, "Carol": 300.0}
