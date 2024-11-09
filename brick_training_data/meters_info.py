# meter_info.py
from utils import write_to_csv, BRICK, UNIT


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


def print_meter_info(meter_info, csv_file_path=None):
    """Print meter information and optionally save to CSV."""
    # Initialize list of rows for CSV
    csv_rows = []

    # Print and save meter information
    print("\nMeter Information:")
    if csv_file_path:
        csv_rows.append(["\nMeter Information:"])

    meter_messages = [
        f"  BTU Meter Present: {meter_info['btu_meter']}",
        f"  Electrical Meter Present: {meter_info['electrical_meter']}",
        f"  Water Meter Present: {meter_info['water_meter']}",
        f"  Gas Meter Present: {meter_info['gas_meter']}",
        f"  PV Meter Present: {meter_info['pv_meter']}",
    ]
    for meter_message in meter_messages:
        print(meter_message)
        if csv_file_path:
            csv_rows.append([meter_message])

    # Write rows to CSV
    if csv_file_path:
        for row in csv_rows:
            write_to_csv(csv_file_path, row)
