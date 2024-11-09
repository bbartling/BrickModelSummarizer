from utils import write_to_csv, BRICK, UNIT


def query_building_area(graph):
    """Query the building area in square feet and handle type information."""
    area_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX unit: <https://qudt.org/vocab/unit#>
    SELECT ?value ?units WHERE {
        ?building a brick:Building ;
                  brick:area ?area .
        ?area brick:hasUnits ?units ;
              brick:value ?value .
    }
    """
    area_results = graph.query(area_query)
    for row in area_results:
        area_value_raw = str(row.value)
        if "^^" in area_value_raw:
            area_value = area_value_raw.split("^^")[0]
        else:
            area_value = area_value_raw

        try:
            area_value = int(area_value)
        except ValueError:
            pass

        area_units = (
            "sq ft"
            if str(row.units) == "http://qudt.org/vocab/unit/FT_2"
            else str(row.units)
        )
        return area_value, area_units

    return None, None


def query_building_floors(graph):
    """Query the number of floors in the building."""
    floors_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(DISTINCT ?floor) AS ?floor_count) WHERE {
        ?floor a brick:Floor .
    }
    """
    floors_results = graph.query(floors_query)
    for row in floors_results:
        return int(row.floor_count)
    return 0


def print_building_info(graph, csv_file_path=None):
    """Print building area and floor count, optionally saving to CSV."""
    csv_rows = []

    building_area, building_units = query_building_area(graph)
    building_floors = query_building_floors(graph)

    area_message = (
        f"Building Area: {building_area} {building_units}"
        if building_area
        else "Building Area information not available."
    )
    floor_message = (
        f"Number of Floors: {building_floors}"
        if building_floors
        else "Floor information not available."
    )

    print(area_message)
    print(floor_message)

    if csv_file_path:
        csv_rows.append([" "])
        csv_rows.append([area_message])
        csv_rows.append([floor_message])
        for row in csv_rows:
            write_to_csv(csv_file_path, row)
