import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS

# Helper function to sanitize URIs
def sanitize_uri(label):
    """Sanitize the label to create a valid URI."""
    return label.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_").replace("%", "")

# Generate BRICK model with external references for timeseries data
def generate_brick_model(csv_columns_mapping, csv_file_name):
    # Define namespaces
    BRICK = Namespace("https://brickschema.org/schema/Brick#")
    EX = Namespace("http://example.com/building#")
    REF = Namespace("https://brickschema.org/schema/Brick/ref#")
    UNIT = Namespace("https://brickschema.org/schema/Brick/unit#")

    # Create an RDF graph
    g = Graph()

    # Bind namespaces
    g.bind("brick", BRICK)
    g.bind("ex", EX)
    g.bind("ref", REF)
    g.bind("unit", UNIT)

    # Define database instance specific to the CSV file
    database_uri = URIRef(f"http://example.com/{sanitize_uri(csv_file_name)}")
    g.add((database_uri, RDF.type, REF.Database))
    g.add((database_uri, RDFS.label, Literal(f"{csv_file_name} Timeseries Storage")))
    g.add((database_uri, URIRef("http://example.com/connstring"), Literal(csv_file_name)))

    # Define entities
    ahu = EX.AHU1
    g.add((ahu, RDF.type, BRICK.Air_Handling_Unit))

    # Add points to the model with external references
    for point, csv_column in csv_columns_mapping.items():
        sanitized_column = sanitize_uri(csv_column)
        point_uri = URIRef(f"http://example.com/building#{sanitized_column}")
        
        # Add point as a type of Brick concept
        g.add((point_uri, RDF.type, URIRef(point)))
        
        # Relate point to the AHU
        g.add((point_uri, BRICK.isPointOf, ahu))
        g.add((ahu, BRICK.hasPoint, point_uri))

        # Add external reference to timeseries data
        timeseries_ref = URIRef(f"http://example.com/timeseries#{sanitized_column}_ref")
        g.add((point_uri, REF.hasExternalReference, timeseries_ref))
        g.add((timeseries_ref, RDF.type, REF.TimeseriesReference))
        g.add((timeseries_ref, REF.hasTimeseriesId, Literal(csv_column)))
        g.add((timeseries_ref, REF.storedAt, database_uri))

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

# Specify the CSV file name
csv_file_name = "building_data.csv"

# Generate and save the BRICK model
brick_graph = generate_brick_model(columns_mapping, csv_file_name)
output_ttl = "brick_model_with_refs.ttl"
brick_graph.serialize(destination=output_ttl, format="turtle")
print(f"BRICK model with timeseries references saved to {output_ttl}.")
