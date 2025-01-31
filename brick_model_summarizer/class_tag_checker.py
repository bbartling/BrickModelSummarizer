import os
from rdflib import Graph
from difflib import get_close_matches, SequenceMatcher


def fetch_and_save_brick_classes():
    """Fetch standard Brick classes from the Brick schema and save to a local file."""
    print("Fetching most current brick tags")
    class_file = "brick_classes.txt"
    brick = Graph()
    brick.parse(
        "https://github.com/BrickSchema/Brick/releases/download/nightly/Brick.ttl",
        format="ttl",
    )

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

    results = brick.query(query)
    class_names = sorted(
        row["preferred"].toPython().replace("https://brickschema.org/schema/Brick#", "")
        for row in results
    )

    with open(class_file, "w") as file:
        file.write("\n".join(class_names))

    print("Saved class tags...")
    return set(class_names)


def fetch_and_save_brick_tags():
    """Fetch standard Brick tags from the Brick schema and save to a local file."""
    print("Fetching most current brick tags")
    tag_file = "brick_tags.txt"
    brick = Graph()
    brick.parse(
        "https://github.com/BrickSchema/Brick/releases/download/nightly/Brick.ttl",
        format="ttl",
    )

    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX tag: <https://brickschema.org/schema/BrickTag#>
    SELECT ?tag ?label WHERE {
        ?tag a brick:Tag .
        ?tag rdfs:label ?label
    }
    """

    results = brick.query(query)
    tag_names = sorted(
        str(row["tag"]).replace("https://brickschema.org/schema/BrickTag#", "")
        for row in results
    )

    with open(tag_file, "w") as file:
        file.write("\n".join(tag_names))

    print("Saved brick tags...")
    return set(tag_names)


def load_brick_classes():
    """Load Brick classes from a local text file or fetch and save them if missing."""
    class_file = "brick_classes.txt"
    return (
        fetch_and_save_brick_classes()
        if not os.path.exists(class_file)
        else set(line.strip() for line in open(class_file))
    )


def load_brick_tags():
    """Load Brick tags from a local text file or fetch and save them if missing."""
    tag_file = "brick_tags.txt"
    return (
        fetch_and_save_brick_tags()
        if not os.path.exists(tag_file)
        else set(line.strip() for line in open(tag_file))
    )


def dump_custom_model_classes(graph):
    """Extract custom Brick model classes from the graph."""
    brick_namespace = "https://brickschema.org/schema/Brick#"
    query = """
    SELECT DISTINCT ?class WHERE {
        ?entity rdf:type ?class .
    }
    """
    results = graph.query(query)
    return sorted(str(row["class"]).replace(brick_namespace, "") for row in results)


def find_similar_classes(custom_classes, standard_classes, cutoff=0.8):
    """Find and compare similar class names between custom and standard classes."""
    mismatches = [
        (cls, matches[0], round(SequenceMatcher(None, cls, matches[0]).ratio(), 2))
        for cls in custom_classes
        if (matches := get_close_matches(cls, standard_classes, n=1, cutoff=cutoff))
        and round(SequenceMatcher(None, cls, matches[0]).ratio(), 2) < 1.00
    ]
    return mismatches


def dump_custom_tags(graph):
    """Retrieve custom tags from the Brick model."""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT DISTINCT ?tag WHERE {
        ?entity brick:tag ?tag .
    }
    """
    results = graph.query(query)
    return sorted(str(row["tag"]) for row in results)


def analyze_classes_and_tags(graph):
    """Analyze custom classes and tags in the Brick model."""
    standard_classes = load_brick_classes()
    standard_tags = load_brick_tags()

    custom_classes = dump_custom_model_classes(graph)
    class_mismatches = find_similar_classes(custom_classes, standard_classes)

    custom_tags = dump_custom_tags(graph)
    tag_mismatches = find_similar_classes(custom_tags, standard_tags)

    print("\nClass Similarities:")
    for custom_class, standard_match, similarity in class_mismatches:
        print(
            f"Similarity ratio between '{custom_class}' and '{standard_match}': {similarity:.2f}"
        )

    return {"class_mismatches": class_mismatches, "tag_mismatches": tag_mismatches}
