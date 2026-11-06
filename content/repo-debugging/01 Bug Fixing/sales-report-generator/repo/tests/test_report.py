from salesreport import build_report
from salesreport.parser import parse_sales
from salesreport.report import top_seller

CSV = (
    "region,rep,amount\n"
    "EU,Alice,100.50\n"
    "eu,Bob,50.25\n"
    "US,Carol,300.00\n"
    "us,Alice,25.00\n"
)


def test_top_seller_is_highest():
    assert top_seller(parse_sales(CSV)) == ("Carol", 300.0)


def test_top_seller_tie_is_alphabetical():
    sales = parse_sales("region,rep,amount\nEU,Bob,100\nEU,Alice,100\n")
    assert top_seller(sales) == ("Alice", 100.0)


def test_top_seller_empty_is_none():
    assert top_seller([]) is None


def test_full_report():
    expected = (
        "Region totals:\n"
        "  EU: 150.75\n"
        "  US: 325.00\n"
        "Top seller: Carol (300.00)"
    )
    assert build_report(CSV) == expected


def test_empty_report():
    assert build_report("region,rep,amount\n") == "No sales."
    assert build_report("") == "No sales."
