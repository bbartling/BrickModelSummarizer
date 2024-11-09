# central_plant_info.py
from utils import write_to_csv, BRICK


def identify_hvac_system_equipment(graph):
    """Combine results from separate queries into a single dictionary for HVAC equipment."""
    hvac_equipment = {}
    hvac_equipment["hvac_system_counts"] = count_hvac_systems(graph)
    hvac_equipment["hvac_features"] = count_hvac_features(graph)
    return hvac_equipment


def count_hvac_systems(graph):
    """Count the total number of chillers, boilers, and cooling towers in the building model."""
    counts = {"chiller_count": 0, "boiler_count": 0, "cooling_tower_count": 0}
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?type (COUNT(?equip) AS ?count) WHERE {
        ?equip a ?type .
        FILTER(?type IN (brick:Chiller, brick:Boiler, brick:Cooling_Tower))
    } GROUP BY ?type
    """
    results = graph.query(query)
    for row in results:
        equip_type = str(row.type)
        count = int(row["count"])
        if equip_type == str(BRICK.Chiller):
            counts["chiller_count"] = count
        elif equip_type == str(BRICK.Boiler):
            counts["boiler_count"] = count
        elif equip_type == str(BRICK.Cooling_Tower):
            counts["cooling_tower_count"] = count
    return counts


def count_hvac_features(graph):
    """Count specific features for chillers, boilers, and cooling towers."""
    features = {
        "chiller_water_flow_count": 0,
        "boiler_water_flow_count": 0,
        "cooling_tower_fan_count": 0,
        "cooling_tower_temp_count": 0,
    }
    # Add queries for each feature if necessary
    # ...

    return features


def print_central_plant_info(hvac_info, csv_file_path=None):
    """Print central plant equipment information and optionally save to CSV."""
    # Initialize list of rows for CSV
    csv_rows = []

    # Print and save central plant counts
    hvac_counts = hvac_info.get("hvac_system_counts", {})
    chiller_message = f"\nTotal Chillers: {hvac_counts.get('chiller_count', 0)}"
    boiler_message = f"Total Boilers: {hvac_counts.get('boiler_count', 0)}"
    cooling_tower_message = (
        f"Total Cooling Towers: {hvac_counts.get('cooling_tower_count', 0)}"
    )
    print(chiller_message)
    print(boiler_message)
    print(cooling_tower_message)
    if csv_file_path:
        csv_rows.append([chiller_message])
        csv_rows.append([boiler_message])
        csv_rows.append([cooling_tower_message])

    # Print and save central plant features if implemented
    hvac_features = hvac_info.get("hvac_features", {})
    feature_messages = [
        f"  Chillers with Water Flow: {hvac_features.get('chiller_water_flow_count', 0)}",
        f"  Boilers with Water Flow: {hvac_features.get('boiler_water_flow_count', 0)}",
        f"  Cooling Towers with Fan: {hvac_features.get('cooling_tower_fan_count', 0)}",
        f"  Cooling Towers with Temp Sensors: {hvac_features.get('cooling_tower_temp_count', 0)}",
    ]
    print("\nCentral Plant Features:")
    if csv_file_path:
        csv_rows.append(["Central Plant Features:"])
    for feature_message in feature_messages:
        print(feature_message)
        if csv_file_path:
            csv_rows.append([feature_message])

    # Write rows to CSV
    if csv_file_path:
        for row in csv_rows:
            write_to_csv(csv_file_path, row)
