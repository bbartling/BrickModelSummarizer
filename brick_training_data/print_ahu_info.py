from rdflib import Graph, Namespace

# Define namespaces
BRICK = Namespace("https://brickschema.org/schema/Brick#")

def load_graph(file_path):
    """Load the RDF graph from a TTL file."""
    graph = Graph()
    graph.parse(file_path, format="turtle")
    return graph

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

def count_ahu_types(graph):
    """Count AHUs by type (Constant Volume or VAV)."""
    cv_count = 0
    vav_count = 0

    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?ahu ?type WHERE {
        ?ahu a brick:Air_Handler_Unit .
        ?ahu a ?type .
        FILTER(?type IN (brick:Constant_Volume_AHU, brick:Variable_Air_Volume_AHU))
    }
    """
    results = graph.query(query)
    for row in results:
        if str(row.type) == str(BRICK.Constant_Volume_AHU):
            cv_count += 1
        elif str(row.type) == str(BRICK.Variable_Air_Volume_AHU):
            vav_count += 1

    return {"cv_count": cv_count, "vav_count": vav_count}

def count_ahu_features(graph):
    """Count AHUs with specific features."""
    cooling_coil_count = 0
    heating_coil_count = 0
    dx_staged_cooling_count = 0
    return_fan_count = 0
    supply_fan_count = 0
    return_temp_count = 0
    mixing_temp_count = 0
    leaving_temp_count = 0
    leaving_air_temp_setpoint_count = 0
    duct_pressure_setpoint_count = 0

    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?ahu ?point WHERE {
        ?ahu a brick:Air_Handler_Unit .
        ?ahu brick:hasPoint ?point .
        FILTER(
            CONTAINS(LCASE(STR(?point)), "cooling_valve_output") ||
            CONTAINS(LCASE(STR(?point)), "heating_valve_output") ||
            CONTAINS(LCASE(STR(?point)), "dx_staged_cooling") ||
            CONTAINS(LCASE(STR(?point)), "return_fan") ||
            CONTAINS(LCASE(STR(?point)), "supply_fan") ||
            CONTAINS(LCASE(STR(?point)), "return_air_temp") ||
            CONTAINS(LCASE(STR(?point)), "mixed_air_temp") ||
            CONTAINS(LCASE(STR(?point)), "supply_air_temp") ||
            CONTAINS(LCASE(STR(?point)), "supply_air_temp_setpoint") ||
            CONTAINS(LCASE(STR(?point)), "supply_air_pressure_setpoint")
        )
    }
    """
    results = graph.query(query)
    for row in results:
        point = str(row.point).lower()
        if "cooling_valve_output" in point:
            cooling_coil_count += 1
        if "heating_valve_output" in point:
            heating_coil_count += 1
        if "dx_staged_cooling" in point:
            dx_staged_cooling_count += 1
        if "return_fan" in point:
            return_fan_count += 1
        if "supply_fan" in point:
            supply_fan_count += 1
        if "return_air_temp" in point:
            return_temp_count += 1
        if "mixed_air_temp" in point:
            mixing_temp_count += 1
        if "supply_air_temp" in point:
            leaving_temp_count += 1
        if "supply_air_temp_setpoint" in point:
            leaving_air_temp_setpoint_count += 1
        if "supply_air_pressure_setpoint" in point:
            duct_pressure_setpoint_count += 1

    return {
        "cooling_coil_count": cooling_coil_count,
        "heating_coil_count": heating_coil_count,
        "dx_staged_cooling_count": dx_staged_cooling_count,
        "return_fan_count": return_fan_count,
        "supply_fan_count": supply_fan_count,
        "return_temp_count": return_temp_count,
        "mixing_temp_count": mixing_temp_count,
        "leaving_temp_count": leaving_temp_count,
        "leaving_air_temp_setpoint_count": leaving_air_temp_setpoint_count,
        "duct_pressure_setpoint_count": duct_pressure_setpoint_count,
    }

def identify_ahu_equipment(graph):
    """Combine results from separate queries into a single AHU equipment dictionary."""
    ahu_equipment = {}
    ahu_equipment["ahu_count"] = count_ahus(graph)
    ahu_equipment["ahu_types"] = count_ahu_types(graph)
    ahu_equipment["ahu_features"] = count_ahu_features(graph)

    return ahu_equipment

def main():
    file_path = "./bldg11.ttl"  # Path to your TTL file
    graph = load_graph(file_path)
    
    # Get AHU equipment information
    ahu_info = identify_ahu_equipment(graph)
    
    # Print the total count of AHUs
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

if __name__ == "__main__":
    main()
