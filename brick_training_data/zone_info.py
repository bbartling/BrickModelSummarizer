# zone_info.py
from brick_utils import BRICK

def identify_zone_equipment(graph):
    """Combine results from separate queries into a single zone equipment dictionary."""
    zone_equipment = {}
    zone_equipment["zone_setpoints"] = query_zone_setpoints(graph)
    zone_equipment["vav_count"] = count_vav_boxes(graph)
    zone_equipment["vav_per_ahu"] = count_vav_boxes_per_ahu(graph)
    zone_equipment["vav_features"] = count_vav_features(graph)
    return zone_equipment

def query_zone_setpoints(graph):
    """Identify zone setpoints relevant to ASO strategies."""
    zone_setpoints = []
    setpoint_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?zone ?point WHERE {
        ?zone a brick:VAV .
        ?zone brick:hasPoint ?point .
        ?point a brick:Zone_Air_Temperature_Setpoint .
    }
    """
    results = graph.query(setpoint_query)
    for row in results:
        zone_setpoints.append(str(row.point))
    return zone_setpoints

def count_vav_boxes(graph):
    """Count the total number of VAV boxes in the building model."""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(?vav) AS ?vav_count) WHERE {
        ?vav a brick:VAV .
    }
    """
    results = graph.query(query)
    for row in results:
        return int(row.vav_count)
    return 0

def count_vav_boxes_per_ahu(graph):
    """Count the number of VAV boxes associated with each AHU."""
    vav_per_ahu = {}
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?ahu (COUNT(?vav) AS ?vav_count) WHERE {
        ?ahu a brick:Air_Handler_Unit .
        ?ahu brick:feeds+ ?vav .
        ?vav a brick:VAV .
    } GROUP BY ?ahu
    """
    results = graph.query(query)
    for row in results:
        ahu_name = str(row.ahu).split("#")[-1]
        vav_per_ahu[ahu_name] = int(row.vav_count)
    return vav_per_ahu


def count_vav_features(graph):
    """Count VAV boxes with specific features."""
    features = {
        "reheat_count": 0,
        "airflow_count": 0,
        "supply_air_temp_count": 0,
        "airflow_setpoint_count": 0,
    }

    # Define the features and corresponding point identifiers
    feature_points = {
        "reheat_count": ["zone_reheat_valve_command"],
        "airflow_count": ["zone_supply_air_flow"],
        "supply_air_temp_count": ["zone_supply_air_temp"],
        "airflow_setpoint_count": ["zone_supply_air_flow_setpoint"],
    }

    for feature, identifiers in feature_points.items():
        for identifier in identifiers:
            query = f"""
            PREFIX brick: <https://brickschema.org/schema/Brick#>
            SELECT (COUNT(DISTINCT ?vav) AS ?count) WHERE {{
                ?vav a brick:VAV ;
                     brick:hasPoint ?point .
                ?point a brick:Point .
                FILTER(CONTAINS(LCASE(STR(?point)), "{identifier.lower()}"))
            }}
            """
            results = graph.query(query)
            for row in results:
                # Convert row["count"] directly
                features[feature] += int(row["count"])

    return features


def print_zone_info(zone_info):
    """Print zone information in a formatted way."""
    zone_setpoints = zone_info.get("zone_setpoints", [])
    if zone_setpoints:
        print("Zone Air Temperature Setpoints Found.")
    else:
        print("No zone air temperature setpoints found.")

    # Print the total count of VAV boxes
    vav_count = zone_info.get("vav_count", 0)
    print(f"Total VAV Boxes: {vav_count}")

    # Print the VAV boxes per AHU
    vav_per_ahu = zone_info.get("vav_per_ahu", {})
    if vav_per_ahu:
        print("Number of VAV Boxes per AHU:")
        for ahu_name, count in vav_per_ahu.items():
            print(f"  AHU: {ahu_name} - VAV Count: {count}")
    else:
        print("No VAV boxes per AHU found.")

    # Print feature-specific counts
    vav_features = zone_info.get("vav_features", {})
    print("\nVAV Box Features:")
    print(f"  VAV Boxes with Reheat Valve Command: {vav_features.get('reheat_count', 0)}")
    print(f"  VAV Boxes with Air Flow Sensors: {vav_features.get('airflow_count', 0)}")
    print(f"  VAV Boxes with Supply Air Temp Sensors: {vav_features.get('supply_air_temp_count', 0)}")
    print(f"  VAV Boxes with Air Flow Setpoints: {vav_features.get('airflow_setpoint_count', 0)}")

    # Calculate and print cooling-only VAV boxes
    cooling_only_vav_count = vav_count - vav_features.get('reheat_count', 0)
    print(f"  Cooling Only VAV Boxes: {cooling_only_vav_count}")
