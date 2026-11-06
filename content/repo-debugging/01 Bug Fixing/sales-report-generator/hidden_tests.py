from salesreport import build_report
from salesreport.aggregate import group_by_region, region_totals, rep_totals
from salesreport.parser import parse_sales
from salesreport.report import top_seller
from salesreport.utils import format_money, parse_amount


def test_three_spellings_one_region():
    sales = parse_sales("region,rep,amount\nEU,A,1\neu,B,2\n Eu ,C,4\n")
    assert region_totals(sales) == {"EU": 7.0}


def test_region_names_reported_uppercase():
    report = build_report("region,rep,amount\nnorth,Ann,10\nNorth,Ben,5\n")
    assert report.splitlines()[1] == "  NORTH: 15.00"


def test_regions_sorted_in_report():
    report = build_report("region,rep,amount\nus,A,1\neu,B,1\napac,C,1\n")
    lines = report.splitlines()
    assert lines[1:4] == ["  APAC: 1.00", "  EU: 1.00", "  US: 1.00"]


def test_top_seller_sums_across_regions():
    csv_text = "region,rep,amount\nEU,Ann,60\nUS,Ann,60\nEU,Ben,100\n"
    assert top_seller(parse_sales(csv_text)) == ("Ann", 120.0)


def test_top_seller_single_sale():
    assert top_seller(parse_sales("region,rep,amount\nEU,Ann,5\n")) == ("Ann", 5.0)


def test_top_seller_with_refunds():
    csv_text = "region,rep,amount\nEU,Ann,100\nEU,Ann,-80\nEU,Ben,10\nEU,Cy,-5\n"
    assert top_seller(parse_sales(csv_text)) == ("Ann", 20.0)  # 100 - 80 still beats 10


def test_top_seller_all_negative():
    csv_text = "region,rep,amount\nEU,Ann,-10\nEU,Ben,-2\n"
    assert top_seller(parse_sales(csv_text)) == ("Ben", -2.0)


def test_top_seller_tie_among_three():
    csv_text = "region,rep,amount\nEU,Cy,50\nEU,Bob,50\nEU,Abe,50\nEU,Dee,10\n"
    assert top_seller(parse_sales(csv_text)) == ("Abe", 50.0)


def test_report_thousands_separator():
    csv_text = 'region,rep,amount\nEU,Ann,"$1,200.50"\neu,Ann,300\n'
    expected = "Region totals:\n  EU: 1,500.50\nTop seller: Ann (1,500.50)"
    assert build_report(csv_text) == expected


def test_report_negative_total_format():
    report = build_report("region,rep,amount\nEU,Ann,-50\n")
    assert report.splitlines()[-1] == "Top seller: Ann (-50.00)"


def test_header_case_and_spacing_ignored():
    sales = parse_sales(" REGION , Rep , AMOUNT \nEU,Ann,3\n")
    assert len(sales) == 1 and sales[0].amount == 3.0


def test_blank_rows_do_not_create_regions():
    sales = parse_sales("region,rep,amount\n,,\nEU,Ann,3\n  ,  ,  \n")
    assert list(group_by_region(sales)) == ["EU"]


def test_invalid_amount_raises():
    try:
        parse_sales("region,rep,amount\nEU,Ann,abc\n")
    except ValueError:
        return
    assert False, "expected ValueError"


def test_rep_totals_preserve_rep_names():
    sales = parse_sales("region,rep,amount\nEU,Ann,1\nUS,Ann,2\nEU,Ben,4\n")
    assert rep_totals(sales) == {"Ann": 3.0, "Ben": 4.0}


def test_utils():
    assert parse_amount(" $1,000 ") == 1000.0
    assert format_money(0) == "0.00"
    assert format_money(1234567.891) == "1,234,567.89"
