import pandas as pd
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF

# Helper function to sanitize URIs
def sanitize_uri(label):
    """Sanitize the label to create a valid URI."""
    return label.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_").replace("%", "")

# Generate BRICK model
def generate_brick_model(csv_columns_mapping):
    # Define namespaces
    BRICK = Namespace("https://brickschema.org/schema/Brick#")
    EX = Namespace("http://example.com/building#")

    # Create an RDF graph
    g = Graph()

    # Bind namespaces
    g.bind("brick", BRICK)
    g.bind("ex", EX)

    # Define entities
    ahu = EX.AHU1
    g.add((ahu, RDF.type, BRICK.Air_Handling_Unit))

    # Add points to the model
    for point, csv_column in csv_columns_mapping.items():
        sanitized_column = sanitize_uri(csv_column)
        point_uri = URIRef(f"http://example.com/building#{sanitized_column}")
        g.add((point_uri, RDF.type, URIRef(point)))
        g.add((point_uri, BRICK.isPointOf, ahu))
        g.add((ahu, BRICK.hasPoint, point_uri))

    # Add fan as part of AHU
    fan = EX.AHU1_Supply_Fan
    g.add((fan, RDF.type, BRICK.Supply_Fan))
    g.add((fan, BRICK.isPartOf, ahu))
    g.add((ahu, BRICK.hasPart, fan))

    return g

# Map CSV columns to BRICK concepts
columns_mapping = {
    "brick:Supply_Air_Static_Pressure_Setpoint": "AHU1_Eff_StaticSPt",
    "brick:Supply_Air_Static_Pressure_Sensor": "AHU1_SaStatic_value (in/wc)",
    "brick:Supply_Fan_Speed_Command": "AHU1_SaFanSpeedAO_value (%)"
}

# Generate and save the BRICK model
brick_graph = generate_brick_model(columns_mapping)
output_ttl = "brick_model.ttl"
brick_graph.serialize(destination=output_ttl, format="turtle")
print(f"BRICK model saved to {output_ttl}.")
