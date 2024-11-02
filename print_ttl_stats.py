from rdflib import Graph, Namespace

# Path to the TTL file
file_path = "./brick_training_data/bldg1.ttl"

# Define namespaces
BRICK = Namespace("https://brickschema.org/schema/Brick#")
NS2 = Namespace("http://buildsys.org/ontologies/bldg1#")  # Adjust based on actual TTL file URI

def load_graph(file_path):
    """Load the RDF graph from a TTL file."""
    graph = Graph()
    graph.parse(file_path, format="turtle")
    return graph

def query_ahu_data(graph):
    """Query the RDF graph to retrieve AHU data."""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX ns2: <http://buildsys.org/ontologies/bldg1#>

    SELECT ?ahu ?predicate ?object WHERE {
        ?ahu a brick:Air_Handler_Unit .
        ?ahu ?predicate ?object .
        FILTER(?predicate IN (brick:hasPoint, brick:feeds, brick:isFedBy))
    }
    """
    
    print("Querying data for all AHUs...")
    results = graph.query(query)

    ahus = {}
    for row in results:
        ahu = str(row.ahu)
        predicate = str(row.predicate)
        object_value = str(row.object)
        
        if ahu not in ahus:
            ahus[ahu] = []

        ahus[ahu].append((predicate, object_value))

    print(f"Total number of AHUs: {len(ahus)}\n")
    return ahus

def display_ahu_data(ahus):
    """Display data for each AHU with potential system type determination."""
    for ahu, points in ahus.items():
        print(f"AHU: {ahu}")
        vav_count = 0
        reheat_count = 0
        for predicate, object_value in points:
            print(f"  Predicate: {predicate}, Object: {object_value}")
            # Check for system types based on point names
            if "VAV" in object_value:
                vav_count += 1
            if "Reheat" in object_value or "HCV" in object_value:
                reheat_count += 1

        # Determine system type based on components found
        if vav_count > 0 and reheat_count > 0:
            system_type = "VAV with Reheat"
        elif vav_count > 0:
            system_type = "VAV System"
        else:
            system_type = "Constant Volume or Other"
        
        print(f"  System Type: {system_type}")
        print("-" * 40)

def count_coil_valves(graph):
    """Count the cooling and heating coil valves for each AHU based on partial matches."""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX ns2: <http://buildsys.org/ontologies/bldg1#>

    SELECT ?ahu ?point WHERE {
        ?ahu a brick:Air_Handler_Unit .
        ?ahu brick:hasPoint ?point .
    }
    """
    
    print("Counting cooling and heating coil valves for each AHU...")
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

    for ahu, counts in ahu_valve_counts.items():
        print(f"AHU: {ahu}")
        print(f"  Cooling Coil Valves (CCV): {counts['CCV_count']}")
        print(f"  Heating Coil Valves (HCV): {counts['HCV_count']}")
        print("-" * 40)
    
    return ahu_valve_counts

def count_building_equipment(graph):
    """Count the number of chillers and boilers in the building."""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX ns2: <http://buildsys.org/ontologies/bldg1#>

    SELECT (COUNT(?chiller) AS ?chiller_count) (COUNT(?boiler) AS ?boiler_count) WHERE {
        OPTIONAL { ?chiller a brick:Chiller . }
        OPTIONAL { ?boiler a brick:Boiler . }
    }
    """
    
    print("Counting chillers and boilers in the building...")
    results = graph.query(query)

    for row in results:
        chiller_count = int(row.chiller_count)
        boiler_count = int(row.boiler_count)
        print(f"Total number of Chillers: {chiller_count}")
        print(f"Total number of Boilers: {boiler_count}")
    
    return {"chiller_count": chiller_count, "boiler_count": boiler_count}

def count_hvac_zones(graph):
    """Count the number of HVAC Zones in the building."""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX ns2: <http://buildsys.org/ontologies/bldg1#>

    SELECT (COUNT(?zone) AS ?zone_count) WHERE {
        ?zone a brick:HVAC_Zone .
    }
    """
    
    print("Counting HVAC Zones in the building...")
    results = graph.query(query)

    for row in results:
        zone_count = int(row.zone_count)
        print(f"Total number of HVAC Zones: {zone_count}")
    
    return {"zone_count": zone_count}

def main():
    graph = load_graph(file_path)
    
    # Query and display AHU data
    ahus = query_ahu_data(graph)
    display_ahu_data(ahus)
    
    # Count and display coil valves for each AHU
    ahu_valve_counts = count_coil_valves(graph)
    
    # Count and display building equipment
    building_equipment_counts = count_building_equipment(graph)
    
    # Count and display HVAC zones
    hvac_zone_counts = count_hvac_zones(graph)

if __name__ == "__main__":
    main()
