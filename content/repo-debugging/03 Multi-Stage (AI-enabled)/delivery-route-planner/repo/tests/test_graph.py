from routeplanner.graph import build_graph
from routeplanner.loader import parse_roads


def _row(origin, destination, distance, unit="km", speed=60.0, **extra):
    row = {
        "origin": origin,
        "destination": destination,
        "distance": distance,
        "unit": unit,
        "speed_kmh": speed,
    }
    row.update(extra)
    return row


def test_km_rows_keep_their_length():
    graph = build_graph([_row("A", "B", 12.0)])
    road = graph.roads_from("A")[0]
    assert road.length_km == 12.0


def test_mile_rows_are_converted_to_km():
    graph = build_graph([_row("A", "B", 10.0, unit="mi")])
    road = graph.roads_from("A")[0]
    assert abs(road.length_km - 16.09344) < 1e-6, road.length_km


def test_roads_are_two_way_by_default():
    graph = build_graph([_row("A", "B", 5.0)])
    assert len(graph.roads_from("B")) == 1
    assert graph.roads_from("B")[0].destination == "A"
    assert graph.road_count() == 2


def test_one_way_row_adds_a_single_direction():
    graph = build_graph([_row("A", "B", 5.0, one_way=True)])
    assert len(graph.roads_from("A")) == 1
    assert len(graph.roads_from("B")) == 0


def test_parse_roads_reads_csv_text():
    text = (
        "origin,destination,distance,unit,speed_kmh,one_way,closed\n"
        "A,B,10,km,50,,\n"
        "B,C,3,mi,40,yes,true\n"
    )
    rows = parse_roads(text)
    assert len(rows) == 2
    assert rows[0]["unit"] == "km" and rows[0]["one_way"] is False
    assert rows[1]["unit"] == "mi" and rows[1]["one_way"] is True
    assert rows[1]["closed"] is True
