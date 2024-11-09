# brick_utils.py
from rdflib import Graph, Namespace
import csv

# Define namespaces
BRICK = Namespace("https://brickschema.org/schema/Brick#")
UNIT = Namespace("https://qudt.org/vocab/unit#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")


def load_graph(file_path):
    """Load the RDF graph from a TTL file."""
    graph = Graph()
    graph.parse(file_path, format="turtle")
    return graph


def write_to_csv(file_path, data):
    """Append data to a CSV file."""
    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)
