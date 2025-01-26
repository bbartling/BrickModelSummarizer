from rdflib import Graph


def list_preferred_brick_classes():
    # Create a graph object
    brick = Graph()

    # Load the Brick ontology from the nightly release
    brick.parse(
        "https://github.com/BrickSchema/Brick/releases/download/nightly/Brick.ttl",
        format="ttl",
    )

    # Define the SPARQL query to list all preferred classes
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX rdf: <http://www.w3.org/1999/02/rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?preferred WHERE {
        ?preferred a owl:Class ;
                   rdfs:subClassOf* brick:Entity .
        FILTER NOT EXISTS { ?preferred brick:aliasOf ?alias }
    }
    """

    # Execute the query
    results = brick.query(query)

    # Collect class names in a list
    class_names = [
        row["preferred"].toPython().replace("https://brickschema.org/schema/Brick#", "")
        for row in results.bindings
    ]

    # Sort the class names alphabetically
    class_names.sort()

    # Write the sorted class names to a text file
    with open("brick_classes.txt", "w") as file:
        for class_name in class_names:
            file.write(class_name + "\n")

    print("Preferred classes saved to 'brick_classes.txt' in sorted order.")


if __name__ == "__main__":
    list_preferred_brick_classes()
