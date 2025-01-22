# meter_info.py
from brick_model_summarizer.utils import BRICK, UNIT


def query_meters(graph):
    """Identify and count all meter types and their associations."""
    meters = {
        "btu_meter": False,
        "electrical_meter": False,
        "water_meter": False,
        "gas_meter": False,
        "pv_meter": False,
        "virtual_meters": 0,
        "submeter_count": 0,
        "metered_entities": {},
    }

    # Query for basic meter types
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?meter ?type WHERE {
        ?meter a ?type .
        FILTER(?type IN (
            brick:BTU_Meter,
            brick:Building_Electric_Meter,
            brick:Water_Meter,
            brick:Gas_Meter,
            brick:PV_Meter
        ))
    }
    """
    results = graph.query(query)
    for row in results:
        meter_type = str(row.type).split("#")[-1]
        if meter_type == "BTU_Meter":
            meters["btu_meter"] = True
        elif meter_type == "Building_Electric_Meter":
            meters["electrical_meter"] = True
        elif meter_type == "Water_Meter":
            meters["water_meter"] = True
        elif meter_type == "Gas_Meter":
            meters["gas_meter"] = True
        elif meter_type == "PV_Meter":
            meters["pv_meter"] = True

    # Add other queries for virtual meters and submeters if needed
    # ...

    return meters


def collect_meter_data(meter_info):
    """
    Collect meter information as structured JSON-compatible data.
    """
    # Prepare meter information with snake_case keys
    meter_data = {
        "btu_meter_present": meter_info.get("btu_meter", "Unknown"),
        "electrical_meter_present": meter_info.get("electrical_meter", "Unknown"),
        "water_meter_present": meter_info.get("water_meter", "Unknown"),
        "gas_meter_present": meter_info.get("gas_meter", "Unknown"),
        "pv_meter_present": meter_info.get("pv_meter", "Unknown"),
    }
    return meter_data
