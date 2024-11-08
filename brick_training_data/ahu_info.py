# ahu_info.py
from brick_utils import BRICK

def identify_ahu_equipment(graph):
    """Combine results from separate queries into a single AHU equipment dictionary."""
    ahu_equipment = {}
    ahu_equipment["ahu_count"] = count_ahus(graph)
    ahu_equipment["ahu_types"] = count_ahu_types(graph)
    ahu_equipment["ahu_features"] = count_ahu_features(graph)
    return ahu_equipment

def count_ahus(graph):
    """Count the total number of AHUs in the building model."""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(?ahu) AS ?ahu_count) WHERE {
        ?ahu a brick:Air_Handler_Unit .
    }
    """
    results = graph.query(query)
    for row in results:
        return int(row.ahu_count)
    return 0

def count_ahu_types(graph):
    """Count AHUs by type (Constant Volume or VAV)."""
    cv_count = 0
    vav_count = 0
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?type (COUNT(?ahu) AS ?count) WHERE {
        ?ahu a brick:Air_Handler_Unit .
        ?ahu a ?type .
        FILTER(?type IN (brick:Constant_Volume_Air_Handler_Unit, brick:Variable_Air_Volume_Air_Handler_Unit))
    } GROUP BY ?type
    """
    results = graph.query(query)
    for row in results:
        ahu_type = str(row.type)
        count = int(row.count)
        if ahu_type == str(BRICK.Constant_Volume_Air_Handler_Unit):
            cv_count = count
        elif ahu_type == str(BRICK.Variable_Air_Volume_Air_Handler_Unit):
            vav_count = count
    return {"cv_count": cv_count, "vav_count": vav_count}



def count_ahu_features(graph):
    """Count AHUs with specific features."""
    features = {
        "cooling_coil_count": 0,
        "heating_coil_count": 0,
        "dx_staged_cooling_count": 0,
        "return_fan_count": 0,
        "supply_fan_count": 0,
        "return_temp_count": 0,
        "mixing_temp_count": 0,
        "leaving_temp_count": 0,
        "leaving_air_temp_setpoint_count": 0,
        "duct_pressure_setpoint_count": 0,
    }

    # Define the features and corresponding point identifiers
    feature_points = {
        "cooling_coil_count": ["cooling_valve_output"],
        "heating_coil_count": ["heating_valve_output"],
        "dx_staged_cooling_count": ["dx_staged_cooling"],
        "return_fan_count": ["return_fan"],
        "supply_fan_count": ["supply_fan"],
        "return_temp_count": ["return_air_temp"],
        "mixing_temp_count": ["mixed_air_temp"],
        "leaving_temp_count": ["supply_air_temp"],
        "leaving_air_temp_setpoint_count": ["supply_air_temp_setpoint"],
        "duct_pressure_setpoint_count": ["supply_air_pressure_setpoint"],
    }

    for feature, identifiers in feature_points.items():
        for identifier in identifiers:
            query = f"""
            PREFIX brick: <https://brickschema.org/schema/Brick#>
            SELECT (COUNT(DISTINCT ?ahu) AS ?count) WHERE {{
                ?ahu a brick:Air_Handler_Unit ;
                     brick:hasPoint ?point .
                ?point a brick:Point .
                FILTER(CONTAINS(LCASE(STR(?point)), "{identifier.lower()}"))
            }}
            """
            results = graph.query(query)
            for row in results:
                # Ensure row["count"] is accessed as a value
                features[feature] += int(row["count"])

    return features



def print_ahu_info(ahu_info):
    """Print AHU information in a formatted way."""
    ahu_count = ahu_info.get("ahu_count", 0)
    print(f"Total AHUs: {ahu_count}")

    # Print AHU types
    ahu_types = ahu_info.get("ahu_types", {})
    print(f"Constant Volume AHUs: {ahu_types.get('cv_count', 0)}")
    print(f"Variable Air Volume AHUs: {ahu_types.get('vav_count', 0)}")

    # Print feature-specific counts
    ahu_features = ahu_info.get("ahu_features", {})
    print("\nAHU Features:")
    print(f"  AHUs with Cooling Coil: {ahu_features.get('cooling_coil_count', 0)}")
    print(f"  AHUs with Heating Coil: {ahu_features.get('heating_coil_count', 0)}")
    print(f"  AHUs with DX Staged Cooling: {ahu_features.get('dx_staged_cooling_count', 0)}")
    print(f"  AHUs with Return Fans: {ahu_features.get('return_fan_count', 0)}")
    print(f"  AHUs with Supply Fans: {ahu_features.get('supply_fan_count', 0)}")
    print(f"  AHUs with Return Air Temp Sensors: {ahu_features.get('return_temp_count', 0)}")
    print(f"  AHUs with Mixing Air Temp Sensors: {ahu_features.get('mixing_temp_count', 0)}")
    print(f"  AHUs with Leaving Air Temp Sensors: {ahu_features.get('leaving_temp_count', 0)}")
    print(f"  AHUs with Leaving Air Temp Setpoint: {ahu_features.get('leaving_air_temp_setpoint_count', 0)}")
    print(f"  AHUs with Duct Pressure Setpoint: {ahu_features.get('duct_pressure_setpoint_count', 0)}")
