from rdflib import Graph
from difflib import get_close_matches, SequenceMatcher


def dump_custom_model_classes(graph):
    brick_namespace = "https://brickschema.org/schema/Brick#"
    query = """
    SELECT DISTINCT ?class WHERE {
        ?entity rdf:type ?class .
    }
    """
    results = graph.query(query)

    # Remove namespace and sort classes
    classes = sorted(
        str(result["class"]).replace(brick_namespace, "") for result in results
    )
    print("\nCustom Brick Entities Found: \n", classes)
    return classes


def list_standard_brick_classes():
    """
    Extracts all standard Brick classes from the nightly release.
    """
    brick_class = []
    brick = Graph()

    # Load the Brick ontology from the nightly release
    brick.parse(
        "https://github.com/BrickSchema/Brick/releases/download/nightly/Brick.ttl",
        format="ttl",
    )

    # SPARQL query to list all preferred classes
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

    for row in results.bindings:
        class_name = (
            row["preferred"]
            .toPython()
            .replace("https://brickschema.org/schema/Brick#", "")
        )
        brick_class.append(class_name)

    return sorted(brick_class)


def normalize_classes(class_list, namespace="https://brickschema.org/schema/Brick#"):
    """
    Normalize class names by stripping namespaces and trimming whitespace.
    """
    return [cls.replace(namespace, "").strip() for cls in class_list]


def find_similar_classes(custom_classes, standard_classes, cutoff=0.8):
    """
    Find similar class names between custom and standard classes and display similarity ratios.
    Exclude exact matches (similarity == 1.00) from the results.
    """
    mismatches = []
    for custom_class in custom_classes:
        matches = get_close_matches(custom_class, standard_classes, n=1, cutoff=cutoff)
        if matches:
            similarity = round(
                SequenceMatcher(None, custom_class, matches[0]).ratio(), 2
            )
            if similarity < 1.00:  # Only append if not an exact match
                print(
                    f"Similarity ratio between '{custom_class}' and '{matches[0]}': {similarity:.2f}"
                )
                mismatches.append((custom_class, matches[0], similarity))

                # Check if the specific match and similarity ratio are found within a tolerance
                if (
                    custom_class == "Air_Handler_Unit"
                    and matches[0] == "Air_Handling_Unit"
                    and 0.84 <= similarity <= 0.86
                ):
                    print(
                        f"Found: Similarity ratio between '{custom_class}' and '{matches[0]}' is {similarity:.2f}: True"
                    )
                else:
                    print(f"Air_Handler_Unit and Air_Handling_Unit NOT FOUND")
        else:
            mismatches.append((custom_class, None, None))
    return mismatches


def dump_custom_tags(graph):
    """
    Retrieves custom tags from the Brick model.
    """
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT DISTINCT ?tag WHERE {
        ?entity brick:tag ?tag .
    }
    """
    results = graph.query(query)

    tags = sorted(str(result["tag"]) for result in results)
    print("tags found: ", tags)
    print("\nCustom Tags Found:")
    for tag in tags:
        print(f"  - {tag}")
    return tags


def list_standard_tags():
    """
    Retrieves the standard tags from the Brick schema.
    """
    standard_tags = []
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
        ?tag    a          brick:Tag .
        ?tag    rdfs:label ?label
    }
    """
    results = brick.query(query)

    for result in results:
        tag = str(result["tag"]).replace("https://brickschema.org/schema/Brick#", "")
        standard_tags.append(tag)

    return sorted(standard_tags)


def analyze_classes_and_tags(graph):
    """Analyze custom classes and tags in the Brick model."""
    # Analyze classes
    custom_model_classes = dump_custom_model_classes(graph)
    raw_standard_model_classes = list_standard_brick_classes()
    standard_model_classes = normalize_classes(raw_standard_model_classes)
    custom_model_classes = normalize_classes(custom_model_classes)
    mismatched_classes = find_similar_classes(
        custom_model_classes, standard_model_classes
    )

    # Dump and check custom tags
    custom_tags = dump_custom_tags(graph)
    standard_tags = list_standard_tags()
    mismatched_tags = find_similar_classes(custom_tags, standard_tags)

    # Print debug information (similarity ratios)
    print("\nClass Similarities:")
    for custom_class, standard_match, similarity in mismatched_classes:
        if standard_match:
            print(
                f"Similarity ratio between '{custom_class}' and '{standard_match}': {similarity:.2f}"
            )

    return {
        "class_mismatches": mismatched_classes,
        "tag_mismatches": mismatched_tags,
    }
