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

def identify_aso_equipment(graph):
    """Identify equipment relevant to ASO strategies."""
    aso_equipment = {
        "btu_meter": False,
        "electrical_meter": False,
        "zone_setpoints": []
    }
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?equip ?type WHERE {
        ?equip a ?type .
        FILTER(?type IN (brick:BTU_Meter, brick:Building_Electric_Meter))
    }
    """
    # Query for BTU and Electrical Meters
    results = graph.query(query)
    for row in results:
        if str(row.type) == str(BRICK.BTU_Meter):
            aso_equipment["btu_meter"] = True
        elif str(row.type) == str(BRICK.Building_Electric_Meter):
            aso_equipment["electrical_meter"] = True

    # Query specifically for zone setpoints with broader search
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
        aso_equipment["zone_setpoints"].append(str(row.point))
    
    return aso_equipment

def analyze_fault_conditions(graph):
    """Analyze AHUs for available data points that enable fault detection."""
    fault_condition_availability = {
        "fault_1_duct_static": False,
        "fault_2_mix_temp_low": False,
        "fault_3_mix_temp_high": False,
        "fault_4_pid_hunting": False,
        # Additional faults can be added here as needed
    }
    
    ahu_data = query_ahu_data(graph)
    
    for ahu, points in ahu_data.items():
        for predicate, obj in points:
            if "Duct_Static_Pressure" in obj and "Fan_Speed" in obj:
                fault_condition_availability["fault_1_duct_static"] = True
            if "Mix_Temperature" in obj and "Outside_Air_Temperature" in obj and "Return_Air_Temperature" in obj:
                fault_condition_availability["fault_2_mix_temp_low"] = True
                fault_condition_availability["fault_3_mix_temp_high"] = True
            if "Operating_Mode" in obj:
                fault_condition_availability["fault_4_pid_hunting"] = True
    
    return fault_condition_availability

def query_meters(graph):
    """Query the RDF graph to retrieve all meters, including virtual meters, submeters, and associated points."""
    meters_info = {
        "meters": [],
        "submeters": [],
        "virtual_meters": []
    }

    # Query for all meters, with labels, types, points, and virtual meter status
    meter_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?meter ?type ?label ?point ?virtual WHERE {
        ?meter a ?type .
        ?meter rdf:type/rdfs:subClassOf* brick:Meter .
        OPTIONAL { ?meter rdfs:label ?label }
        OPTIONAL { ?point brick:isPointOf ?meter }
        OPTIONAL { ?meter brick:isVirtualMeter/brick:value ?virtual }
    }
    """
    results = graph.query(meter_query)
    
    for row in results:
        meter = str(row.meter)
        meter_type = str(row.type)
        label = str(row.label) if row.label else "No Label"
        point = str(row.point) if row.point else None
        is_virtual = bool(row.virtual) if row.virtual else False

        # Structure each meter's information
        meter_info = {
            "meter_id": meter,
            "type": meter_type,
            "label": label,
            "is_virtual": is_virtual,
            "associated_points": []
        }
        
        # Append the meter details if not already added
        if meter not in [m['meter_id'] for m in meters_info["meters"]]:
            meters_info["meters"].append(meter_info)
        
        # Update with point information if applicable
        for m in meters_info["meters"]:
            if m["meter_id"] == meter and point:
                m["associated_points"].append(point)
                break

        # Categorize as virtual meter if applicable
        if is_virtual:
            meters_info["virtual_meters"].append(meter)

    # Query for submeters and their relationships
    submeter_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?meter ?submeter WHERE {
        ?meter rdf:type/rdfs:subClassOf* brick:Meter .
        ?meter brick:hasSubMeter ?submeter .
    }
    """
    submeter_results = graph.query(submeter_query)
    for row in submeter_results:
        meter = str(row.meter)
        submeter = str(row.submeter)
        meters_info["submeters"].append((meter, submeter))
    
    return meters_info

def print_meter_info(meters_info):
    """Print detailed information about all meters, virtual meters, submeters, and photovoltaic arrays."""
    print("Building Metering Information:")
    print(f"Total Meters Found: {len(meters_info['meters'])}")
    print(f"Virtual Meters Count: {len(meters_info['virtual_meters'])}")
    
    print("Submeter Relationships:")
    if meters_info["submeters"]:
        for meter, submeter in meters_info["submeters"]:
            print(f"  Meter: {meter} has Submeter: {submeter}")
    else:
        print("  No submeter relationships found.")
    
    print("\nDetailed Meter List:")
    if meters_info["meters"]:
        for meter in meters_info["meters"]:
            print(f"Meter ID: {meter['meter_id']}")
            print(f"  Type: {meter['type']}")
            print(f"  Label: {meter['label']}")
            print(f"  Virtual Meter: {'Yes' if meter['is_virtual'] else 'No'}")
            print(f"  Associated Points: {', '.join(meter['associated_points']) if meter['associated_points'] else 'None'}")
            print("-" * 40)
    else:
        print("No meters found in the model.")

def query_pv_arrays(graph):
    """Query the RDF graph to retrieve photovoltaic arrays and their associated panels."""
    pv_arrays = {}

    # Query for PV Arrays and associated PV Panels
    pv_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?array ?panel WHERE {
        ?array a brick:PV_Array .
        ?panel a brick:PV_Panel .
        ?panel brick:isPartOf ?array .
    }
    """
    results = graph.query(pv_query)
    for row in results:
        array = str(row.array)
        panel = str(row.panel)
        
        if array not in pv_arrays:
            pv_arrays[array] = []
        pv_arrays[array].append(panel)
    
    return pv_arrays

def print_building_measures(graph, file_path):
    """Print out building measures based on ASO potential and fault detection capability."""
    print(f"\nAnalyzing building model from: {file_path}")

    # Extract AHU data
    ahus = query_ahu_data(graph)
    print(f"Total AHUs: {len(ahus)}")
    
    # Identify ASO relevant equipment
    aso_equipment = identify_aso_equipment(graph)
    print("ASO Equipment Available:")
    print(f"  BTU Meter: {'Yes' if aso_equipment['btu_meter'] else 'No'}")
    print(f"  Electrical Meter: {'Yes' if aso_equipment['electrical_meter'] else 'No'}")
    print(f"  Zone Setpoints Count: {len(aso_equipment['zone_setpoints'])}")
    
    # Check for AHUs with fault detection point availability
    fault_conditions = analyze_fault_conditions(graph)
    print("Fault Detection Availability:")
    for fault, available in fault_conditions.items():
        print(f"  {fault}: {'Available' if available else 'Not Available'}")
    
    # Additional measures for rogue zone analysis and duct static pressure trim
    vav_systems = [ahu for ahu, points in ahus.items() if any("VAV" in p[1] for p in points)]
    print(f"Total VAV AHUs (for rogue zone analysis): {len(vav_systems)}")

    # Check for load management potential based on identified equipment
    if aso_equipment["electrical_meter"]:
        print("Building has an electrical meter - potential for demand limiting, shifting, or shed strategies.")
    
    if aso_equipment["zone_setpoints"]:
        print("Zone setpoints detected - potential for dynamic load adjustment per zone demand.")
    
    # Query and print meter information
    meters_info = query_meters(graph)
    print("\nBuilding Metering Information:")
    print(f"Total Meters Found: {len(meters_info['meters'])}")
    print(f"Virtual Meters Count: {len(meters_info['virtual_meters'])}")
    print("Submeter Relationships:")
    for meter, submeter in meters_info["submeters"]:
        print(f"  Meter: {meter} has Submeter: {submeter}")
    
    print("\nDetailed Meter List:")
    for meter in meters_info["meters"]:
        print(f"Meter ID: {meter['meter_id']}")
        print(f"  Type: {meter['type']}")
        print(f"  Virtual Meter: {'Yes' if meter['is_virtual'] else 'No'}")
        print(f"  Associated Points: {', '.join(meter['associated_points']) if meter['associated_points'] else 'None'}")
        print("-" * 40)

    # Query and print photovoltaic arrays and panels
    pv_arrays = query_pv_arrays(graph)
    print("\nPhotovoltaic Arrays Information:")
    if pv_arrays:
        for array, panels in pv_arrays.items():
            print(f"PV Array ID: {array}")
            print(f"  Panels: {', '.join(panels)}")
    else:
        print("No photovoltaic arrays found.")

def main():
    file_path = "./bldg11.ttl"  # Path to your TTL file
    graph = load_graph(file_path)
    
    # Print building measures based on BRICK model analysis
    print_building_measures(graph, file_path)

if __name__ == "__main__":
    main()
