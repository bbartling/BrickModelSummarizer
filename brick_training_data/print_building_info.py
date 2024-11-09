from rdflib import Graph, Namespace, Literal, URIRef

# Define namespaces
BRICK = Namespace("https://brickschema.org/schema/Brick#")
UNIT = Namespace("https://qudt.org/vocab/unit#")


def load_graph(file_path):
    """Load the RDF graph from a TTL file."""
    graph = Graph()
    graph.parse(file_path, format="turtle")
    return graph


def query_building_area(graph):
    """Query the building area in square feet and handle type information."""
    area_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX unit: <https://qudt.org/vocab/unit#>
    SELECT ?value ?units WHERE {
        ?building a brick:Building ;
                  brick:area ?area .
        ?area brick:hasUnits ?units ;
              brick:value ?value .
    }
    """
    area_results = graph.query(area_query)
    for row in area_results:
        print("Debug - Retrieved row:", row)

        # Extract the area value, removing type information if necessary
        area_value_raw = str(row.value)
        if "^^" in area_value_raw:
            area_value = area_value_raw.split("^^")[0]  # Remove the type suffix
        else:
            area_value = area_value_raw

        # Ensure area_value is an integer if possible
        try:
            area_value = int(area_value)
        except ValueError:
            pass

        # Replace the full URI with "sq ft" if it's for square feet
        area_units = (
            "FT_2"
            if str(row.units) == "http://qudt.org/vocab/unit/FT_2"
            else str(row.units)
        )

        print(f"Building Area: {area_value}")
        print(f"Units: {area_units}")

        return area_value, area_units

    print("No building area information found.")
    return None, None


def query_building_floors(graph):
    """Query the number of floors in the building."""
    floors_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(DISTINCT ?floor) AS ?floor_count) WHERE {
        ?floor a brick:Floor .
    }
    """
    floors_results = graph.query(floors_query)
    for row in floors_results:
        return int(row.floor_count)
    return 0


def main():
    file_path = "./files/bldg6.ttl"  # Path to your TTL file
    graph = load_graph(file_path)

    # Query building area and floor count
    building_area, building_units = query_building_area(graph)
    building_floors = query_building_floors(graph)

    # Print building information
    area_message = (
        f"Building Area: {building_area} {building_units}"
        if building_area
        else "Building Area information not available."
    )
    floor_message = (
        f"Number of Floors: {building_floors}"
        if building_floors
        else "Floor information not available."
    )
    print(area_message)
    print(floor_message)


if __name__ == "__main__":
    main()
