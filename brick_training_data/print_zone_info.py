from rdflib import Graph, Namespace

# Define namespaces
BRICK = Namespace("https://brickschema.org/schema/Brick#")

def load_graph(file_path):
    """Load the RDF graph from a TTL file."""
    graph = Graph()
    graph.parse(file_path, format="turtle")
    return graph

def query_zone_setpoints(graph):
    """Identify zone setpoints relevant to ASO strategies."""
    zone_setpoints = []

    setpoint_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?zone ?point WHERE {
        ?zone a brick:VAV .
        ?zone brick:hasPoint ?point .
        FILTER(CONTAINS(LCASE(STR(?point)), "zone_air_temp_setpoint"))
    }
    """
    setpoint_results = graph.query(setpoint_query)
    for row in setpoint_results:
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

def count_vav_boxes_per_ahu(graph):
    """Count the number of VAV boxes associated with each AHU."""
    vav_per_ahu = {}

    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?ahu (COUNT(?vav) AS ?vav_count) WHERE {
        ?ahu a brick:Air_Handler_Unit .
        ?ahu brick:feeds ?vav .
        ?vav a brick:VAV .
    } GROUP BY ?ahu
    """

    results = graph.query(query)
    for row in results:
        vav_per_ahu[str(row.ahu)] = int(row.vav_count)

    return vav_per_ahu

def count_vav_features(graph):
    """Count VAV boxes with specific features like reheat valve, air flow, and supply air temp sensors."""
    reheat_count = 0
    airflow_count = 0
    supply_air_temp_count = 0

    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?vav ?point WHERE {
        ?vav a brick:VAV .
        ?vav brick:hasPoint ?point .
        FILTER(
            CONTAINS(LCASE(STR(?point)), "zone_reheat_valve_command") ||
            CONTAINS(LCASE(STR(?point)), "zone_supply_air_flow") ||
            CONTAINS(LCASE(STR(?point)), "zone_supply_air_temp")
        )
    }
    """

    results = graph.query(query)
    for row in results:
        point = str(row.point).lower()
        if "zone_reheat_valve_command" in point:
            reheat_count += 1
        if "zone_supply_air_flow" in point:
            airflow_count += 1
        if "zone_supply_air_temp" in point:
            supply_air_temp_count += 1

    return {
        "reheat_count": reheat_count,
        "airflow_count": airflow_count,
        "supply_air_temp_count": supply_air_temp_count
    }

def identify_zone_equipment(graph):
    """Combine results from separate queries into a single ASO equipment dictionary."""
    zone_equipment = {}
    zone_equipment["zone_setpoints"] = query_zone_setpoints(graph)
    zone_equipment["vav_count"] = count_vav_boxes(graph)
    zone_equipment["vav_per_ahu"] = count_vav_boxes_per_ahu(graph)
    zone_equipment["vav_features"] = count_vav_features(graph)

    return zone_equipment

def main():
    file_path = "./bldg11.ttl"  # Path to your TTL file
    graph = load_graph(file_path)
    
    # Get ASO equipment information
    zone_info = identify_zone_equipment(graph)
    
    # Print only the zone setpoints in a more detailed manner
    zone_setpoints = zone_info.get("zone_setpoints", [])
    if zone_setpoints:
        print("Zone Air Temperature Setpoints Found.")
    else:
        print("No zone air temperature setpoints found.")
    
    # Print the total count of VAV boxes
    vav_count = zone_info.get("vav_count", 0)
    print(f"Total VAV Boxes: {vav_count}")
    
    # Print the VAV boxes per AHU with shortened AHU names
    vav_per_ahu = zone_info.get("vav_per_ahu", {})
    if vav_per_ahu:
        print("Number of VAV Boxes per AHU:")
        for ahu_uri, count in vav_per_ahu.items():
            # Extract AHU name after the '#' symbol
            ahu_name = ahu_uri.split("#")[-1]
            print(f"  AHU: {ahu_name} - VAV Count: {count}")
    else:
        print("No VAV boxes per AHU found.")
    
    # Print feature-specific counts
    vav_features = zone_info.get("vav_features", {})
    print("\nVAV Box Features:")
    print(f"  VAV Boxes with Reheat Valve Command: {vav_features.get('reheat_count', 0)}")
    print(f"  VAV Boxes with Air Flow Sensors: {vav_features.get('airflow_count', 0)}")
    print(f"  VAV Boxes with Supply Air Temp Sensors: {vav_features.get('supply_air_temp_count', 0)}")

if __name__ == "__main__":
    main()
