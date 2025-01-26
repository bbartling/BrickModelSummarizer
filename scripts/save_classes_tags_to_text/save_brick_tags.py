from rdflib import Graph


def list_standard_brick_tags():
    # Create a graph object
    brick = Graph()

    # Load the Brick ontology
    print("Loading Brick ontology...")
    brick.parse(
        "https://github.com/BrickSchema/Brick/releases/download/nightly/Brick.ttl",
        format="ttl",
    )
    print(f"Number of triples loaded: {len(brick)}")

    # SPARQL query to list Brick tags
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX tag: <https://brickschema.org/schema/BrickTag#>

    SELECT ?tag ?label WHERE {
        ?tag    a          brick:Tag .
        ?tag    rdfs:label ?label
    }
    """

    # Execute the query
    results = brick.query(query)

    # Collect tag names
    tag_names = []

    if results:
        for row in results:
            tag_uri = str(row["tag"])

            # Remove prefix
            tag_name = tag_uri.replace("https://brickschema.org/schema/BrickTag#", "")

            # Add tag name to the list
            tag_names.append(tag_name)
    else:
        print("No tags found in the query results.")

    # Sort the tag names alphabetically
    tag_names.sort()

    # Save the sorted tag names to a file
    with open("brick_tags.txt", "w") as file:
        for tag_name in tag_names:
            file.write(tag_name + "\n")

    print("Sorted tags saved to 'brick_tags.txt'.")


if __name__ == "__main__":
    list_standard_brick_tags()
