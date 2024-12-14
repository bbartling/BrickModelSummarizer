# meter_info.py
from utils import BRICK, UNIT


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
    Collect meter information as structured data.
    """
    # Prepare meter information
    meter_data = {
        "BTU Meter Present": meter_info.get("btu_meter", "Unknown"),
        "Electrical Meter Present": meter_info.get("electrical_meter", "Unknown"),
        "Water Meter Present": meter_info.get("water_meter", "Unknown"),
        "Gas Meter Present": meter_info.get("gas_meter", "Unknown"),
        "PV Meter Present": meter_info.get("pv_meter", "Unknown"),
    }
    return meter_data

