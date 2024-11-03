import csv
from rdflib import Graph, Namespace

# Define namespaces
BRICK = Namespace("https://brickschema.org/schema/Brick#")
NS2 = Namespace("http://buildsys.org/ontologies/bldg#")  # Adjust based on actual TTL file URI

def load_graph(file_path):
    """Load the RDF graph from a TTL file."""
    graph = Graph()
    graph.parse(file_path, format="turtle")
    return graph

def query_ahu_data(graph):
    """Query the RDF graph to retrieve AHU data."""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?ahu ?predicate ?object WHERE {
        ?ahu a brick:Air_Handler_Unit .
        ?ahu ?predicate ?object .
        FILTER(?predicate IN (brick:hasPoint, brick:feeds, brick:isFedBy))
    }
    """
    
    results = graph.query(query)
    ahus = {}
    for row in results:
        ahu = str(row.ahu)
        predicate = str(row.predicate)
        object_value = str(row.object)
        
        if ahu not in ahus:
            ahus[ahu] = []

        ahus[ahu].append((predicate, object_value))
    
    return ahus

def count_coil_valves(graph):
    """Count the cooling and heating coil valves for each AHU based on partial matches."""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?ahu ?point WHERE {
        ?ahu a brick:Air_Handler_Unit .
        ?ahu brick:hasPoint ?point .
    }
    """
    
    results = graph.query(query)
    ahu_valve_counts = {}
    for row in results:
        ahu = str(row.ahu)
        point = str(row.point)

        if ahu not in ahu_valve_counts:
            ahu_valve_counts[ahu] = {"CCV_count": 0, "HCV_count": 0}

        if "Cooling" in point or "CCV" in point:
            ahu_valve_counts[ahu]["CCV_count"] += 1
        elif "Heating" in point or "HCV" in point:
            ahu_valve_counts[ahu]["HCV_count"] += 1
    
    return ahu_valve_counts

def count_building_equipment(graph):
    """Count the number of chillers and boilers in the building."""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(?chiller) AS ?chiller_count) (COUNT(?boiler) AS ?boiler_count) WHERE {
        OPTIONAL { ?chiller a brick:Chiller . }
        OPTIONAL { ?boiler a brick:Boiler . }
    }
    """
    
    results = graph.query(query)
    row = next(iter(results))
    chiller_count = int(row.chiller_count)
    boiler_count = int(row.boiler_count)
    
    return {"chiller_count": chiller_count, "boiler_count": boiler_count}

def count_hvac_zones(graph):
    """Count the number of HVAC Zones in the building."""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(?zone) AS ?zone_count) WHERE {
        ?zone a brick:HVAC_Zone .
    }
    """
    
    results = graph.query(query)
    row = next(iter(results))
    zone_count = int(row.zone_count)
    
    return {"zone_count": zone_count}

def determine_building_prototype(data):
    """Classify building type based on equipment characteristics."""
    # Basic heuristic based on counts (this can be refined based on actual standards)
    if data["total_ahus"] <= 2 and data["total_chillers"] <= 1:
        data["building_type"] = "Small Office"
    elif data["total_ahus"] <= 4 and data["total_chillers"] <= 2:
        data["building_type"] = "Medium Office"
    elif data["total_ahus"] > 4:
        data["building_type"] = "Large Office"
    # Additional building type rules can be added here

def extract_building_data(graph, file_path):
    """Extract and organize building data for labeling."""
    building_data = {
        "file": file_path,
        "total_ahus": 0,
        "total_chillers": 0,
        "total_boilers": 0,
        "total_zones": 0,
        "ahu_data": []
    }
    
    # Query for AHU data
    ahus = query_ahu_data(graph)
    building_data["total_ahus"] = len(ahus)
    
    # Count coil valves
    ahu_valve_counts = count_coil_valves(graph)
    
    # Count chillers and boilers
    equipment_counts = count_building_equipment(graph)
    building_data["total_chillers"] = equipment_counts["chiller_count"]
    building_data["total_boilers"] = equipment_counts["boiler_count"]
    
    # Count HVAC zones
    hvac_zone_counts = count_hvac_zones(graph)
    building_data["total_zones"] = hvac_zone_counts["zone_count"]
    
    # Process each AHU's details for system type classification
    for ahu, points in ahus.items():
        ahu_info = {"ahu_id": ahu, "system_type": "", "points": []}
        vav_count, reheat_count = 0, 0
        for predicate, obj in points:
            if "VAV" in obj:
                vav_count += 1
            if "Reheat" in obj or "HCV" in obj:
                reheat_count += 1
            ahu_info["points"].append((predicate, obj))
        
        # Determine the system type based on VAV and reheat counts
        if vav_count > 0 and reheat_count > 0:
            ahu_info["system_type"] = "VAV with Reheat"
        elif vav_count > 0:
            ahu_info["system_type"] = "VAV System"
        else:
            ahu_info["system_type"] = "Constant Volume or Other"
        
        building_data["ahu_data"].append(ahu_info)
    
    # Determine building prototype based on equipment counts
    determine_building_prototype(building_data)
    
    return building_data

def save_as_csv(data, output_path="building_data.csv"):
    """Save structured building data to CSV for BERT training."""
    with open(output_path, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        if csv_file.tell() == 0:  # Write header if file is new
            writer.writerow(["file", "total_ahus", "total_chillers", "total_boilers", 
                             "total_zones", "building_type", "ahu_data"])
        # Serialize AHU data to a simpler format
        ahu_data_serialized = "; ".join(
            [f"{ahu['ahu_id']} ({ahu['system_type']})" for ahu in data["ahu_data"]]
        )
        writer.writerow([data["file"], data["total_ahus"], data["total_chillers"], 
                         data["total_boilers"], data["total_zones"], data["building_type"], 
                         ahu_data_serialized])

def main():
    # Load graph for each TTL file (simulate a directory with multiple files)
    for i in range(1, 43):  # For each building TTL file
        file_path = f"./bldg{i}.ttl"
        graph = load_graph(file_path)
        
        # Extract building data and save to labeled dataset
        building_data = extract_building_data(graph, file_path)
        save_as_csv(building_data)

if __name__ == "__main__":
    main()
