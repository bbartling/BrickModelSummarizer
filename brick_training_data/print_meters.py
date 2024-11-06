from rdflib import Graph, Namespace

# Define namespaces
BRICK = Namespace("https://brickschema.org/schema/Brick#")

def load_graph(file_path):
    """Load the RDF graph from a TTL file."""
    graph = Graph()
    graph.parse(file_path, format="turtle")
    return graph

def query_meters(graph):
    """Identify and count all meter types and their associations."""
    meters = {
        "btu_meter": False,
        "electrical_meter": False,
        "water_meter": False,
        "gas_meter": False,
        "virtual_meters": 0,
        "pv_meter": False,
        "submeter_count": 0,
        "metered_entities": {}
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
        meter_type = str(row.type)
        if meter_type == str(BRICK.BTU_Meter):
            meters["btu_meter"] = True
        elif meter_type == str(BRICK.Building_Electric_Meter):
            meters["electrical_meter"] = True
        elif meter_type == str(BRICK.Water_Meter):
            meters["water_meter"] = True
        elif meter_type == str(BRICK.Gas_Meter):
            meters["gas_meter"] = True
        elif meter_type == str(BRICK.PV_Meter):
            meters["pv_meter"] = True

    # Query for virtual meters
    virtual_meter_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(?meter) AS ?virtual_count) WHERE {
        ?meter a brick:Meter .
        ?meter brick:isVirtualMeter [ brick:value true ] .
    }
    """
    virtual_results = graph.query(virtual_meter_query)
    for row in virtual_results:
        meters["virtual_meters"] = int(row.virtual_count)

    # Query for submeters
    submeter_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(?submeter) AS ?submeter_count) WHERE {
        ?meter a brick:Meter .
        ?meter brick:hasSubMeter ?submeter .
    }
    """
    submeter_results = graph.query(submeter_query)
    for row in submeter_results:
        meters["submeter_count"] = int(row.submeter_count)

    # Query for metered entities
    metered_entity_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?entity ?meter WHERE {
        ?entity brick:isMeteredBy ?meter .
        ?meter rdf:type/rdfs:subClassOf* brick:Meter .
    }
    """
    metered_entity_results = graph.query(metered_entity_query)
    for row in metered_entity_results:
        entity = str(row.entity)
        meter = str(row.meter)
        if meter not in meters["metered_entities"]:
            meters["metered_entities"][meter] = []
        meters["metered_entities"][meter].append(entity)

    return meters

def query_pv_arrays(graph):
    """Identify PV Arrays and associated panels or generation systems."""
    pv_arrays = {"pv_array_count": 0, "pv_generation_systems": 0, "pv_panels": 0}

    # Count PV Arrays
    pv_array_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(?array) AS ?array_count) WHERE {
        ?array a brick:PV_Array .
    }
    """
    array_results = graph.query(pv_array_query)
    for row in array_results:
        pv_arrays["pv_array_count"] = int(row.array_count)

    # Count PV Generation Systems
    pv_gen_system_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(?system) AS ?system_count) WHERE {
        ?system a brick:PV_Generation_System .
    }
    """
    gen_system_results = graph.query(pv_gen_system_query)
    for row in gen_system_results:
        pv_arrays["pv_generation_systems"] = int(row.system_count)

    # Count PV Panels
    pv_panel_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(?panel) AS ?panel_count) WHERE {
        ?panel a brick:PV_Panel .
    }
    """
    panel_results = graph.query(pv_panel_query)
    for row in panel_results:
        pv_arrays["pv_panels"] = int(row.panel_count)

    return pv_arrays

def main():
    file_path = "./bldg11.ttl"  # Path to your TTL file
    graph = load_graph(file_path)
    
    # Get meter information
    meter_info = query_meters(graph)
    print("Meter Information:")
    print(f"  BTU Meter Present: {meter_info['btu_meter']}")
    print(f"  Electrical Meter Present: {meter_info['electrical_meter']}")
    print(f"  Water Meter Present: {meter_info['water_meter']}")
    print(f"  Gas Meter Present: {meter_info['gas_meter']}")
    print(f"  PV Meter Present: {meter_info['pv_meter']}")
    print(f"  Virtual Meters Count: {meter_info['virtual_meters']}")
    print(f"  Submeter Count: {meter_info['submeter_count']}")
    
    print("\nMetered Entities:")
    for meter, entities in meter_info["metered_entities"].items():
        print(f"  Meter: {meter}")
        for entity in entities:
            print(f"    - {entity}")

    # Get PV array information
    pv_info = query_pv_arrays(graph)
    print("\nPV Array Information:")
    print(f"  PV Arrays Count: {pv_info['pv_array_count']}")
    print(f"  PV Generation Systems Count: {pv_info['pv_generation_systems']}")
    print(f"  PV Panels Count: {pv_info['pv_panels']}")

if __name__ == "__main__":
    main()
