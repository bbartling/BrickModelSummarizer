from rdflib import Graph, Namespace

# Define namespaces
BRICK = Namespace("https://brickschema.org/schema/Brick#")

def load_graph(file_path):
    """Load the RDF graph from a TTL file."""
    graph = Graph()
    graph.parse(file_path, format="turtle")
    return graph

def count_hvac_systems(graph):
    """Count the total number of chillers, boilers, and cooling towers in the building model."""
    counts = {
        "chiller_count": 0,
        "boiler_count": 0,
        "cooling_tower_count": 0
    }

    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?equip ?type WHERE {
        ?equip a ?type .
        FILTER(?type IN (brick:Chiller, brick:Boiler, brick:Cooling_Tower))
    }
    """
    results = graph.query(query)
    for row in results:
        if str(row.type) == str(BRICK.Chiller):
            counts["chiller_count"] += 1
        elif str(row.type) == str(BRICK.Boiler):
            counts["boiler_count"] += 1
        elif str(row.type) == str(BRICK.Cooling_Tower):
            counts["cooling_tower_count"] += 1

    return counts

def count_hvac_features(graph):
    """Count specific features for chillers, boilers, and cooling towers."""
    chiller_water_flow_count = 0
    boiler_water_flow_count = 0
    cooling_tower_fan_count = 0
    cooling_tower_temp_count = 0

    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?equip ?point WHERE {
        ?equip a ?type .
        ?equip brick:hasPoint ?point .
        FILTER(
            (CONTAINS(LCASE(STR(?point)), "chilled_water_flow") && ?type = brick:Chiller) ||
            (CONTAINS(LCASE(STR(?point)), "boiler_water_flow") && ?type = brick:Boiler) ||
            (CONTAINS(LCASE(STR(?point)), "cooling_tower_fan") && ?type = brick:Cooling_Tower) ||
            (CONTAINS(LCASE(STR(?point)), "cooling_tower_temp") && ?type = brick:Cooling_Tower)
        )
    }
    """
    results = graph.query(query)
    for row in results:
        point = str(row.point).lower()
        if "chilled_water_flow" in point:
            chiller_water_flow_count += 1
        if "boiler_water_flow" in point:
            boiler_water_flow_count += 1
        if "cooling_tower_fan" in point:
            cooling_tower_fan_count += 1
        if "cooling_tower_temp" in point:
            cooling_tower_temp_count += 1

    return {
        "chiller_water_flow_count": chiller_water_flow_count,
        "boiler_water_flow_count": boiler_water_flow_count,
        "cooling_tower_fan_count": cooling_tower_fan_count,
        "cooling_tower_temp_count": cooling_tower_temp_count
    }

def identify_hvac_system_equipment(graph):
    """Combine results from separate queries into a single dictionary for HVAC equipment."""
    hvac_equipment = {}
    hvac_equipment["hvac_system_counts"] = count_hvac_systems(graph)
    hvac_equipment["hvac_features"] = count_hvac_features(graph)

    return hvac_equipment

def main():
    file_path = "./bldg11.ttl"  # Path to your TTL file
    graph = load_graph(file_path)
    
    # Get HVAC system equipment information
    hvac_info = identify_hvac_system_equipment(graph)
    
    # Print the counts of HVAC systems
    hvac_counts = hvac_info.get("hvac_system_counts", {})
    print(f"Total Chillers: {hvac_counts.get('chiller_count', 0)}")
    print(f"Total Boilers: {hvac_counts.get('boiler_count', 0)}")
    print(f"Total Cooling Towers: {hvac_counts.get('cooling_tower_count', 0)}")
    
    # Print feature-specific counts
    hvac_features = hvac_info.get("hvac_features", {})
    print("\nHVAC System Features:")
    print(f"  Chillers with Chilled Water Flow Sensors: {hvac_features.get('chiller_water_flow_count', 0)}")
    print(f"  Boilers with Boiler Water Flow Sensors: {hvac_features.get('boiler_water_flow_count', 0)}")
    print(f"  Cooling Towers with Fan Sensors: {hvac_features.get('cooling_tower_fan_count', 0)}")
    print(f"  Cooling Towers with Temperature Sensors: {hvac_features.get('cooling_tower_temp_count', 0)}")

if __name__ == "__main__":
    main()
