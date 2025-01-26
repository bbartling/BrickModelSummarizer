from brick_model_summarizer.utils import BRICK, UNIT


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


def query_hvac_equipment(graph):
    """Query the number of HVAC equipment in the building."""
    hvac_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(DISTINCT ?equipment) AS ?equipment_count) WHERE {
        ?equipment a brick:HVAC_Equipment .
    }
    """
    hvac_results = graph.query(hvac_query)
    for row in hvac_results:
        return int(row.equipment_count)
    return 0


def query_hvac_zones(graph):
    """Query the number of HVAC zones in the building."""
    hvac_zone_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(DISTINCT ?zone) AS ?zone_count) WHERE {
        ?zone a brick:HVAC_Zone .
    }
    """
    hvac_zone_results = graph.query(hvac_zone_query)
    for row in hvac_zone_results:
        return int(row.zone_count)
    return 0


def collect_building_data(graph):
    """
    Collect building area, floor count, HVAC equipment, and HVAC zones as structured JSON-compatible data.
    """
    building_data = {}
    building_area, building_units = query_building_area(graph)
    building_floors = query_building_floors(graph)
    hvac_equipment_count = query_hvac_equipment(graph)
    hvac_zone_count = query_hvac_zones(graph)

    if building_area:
        building_data["building_area"] = f"{building_area} {building_units}"
    else:
        building_data["building_area"] = "not_available"

    if building_floors:
        building_data["number_of_floors"] = building_floors
    else:
        building_data["number_of_floors"] = "not_available"

    building_data["hvac_equipment_count"] = hvac_equipment_count
    building_data["hvac_zone_count"] = hvac_zone_count

    return building_data
