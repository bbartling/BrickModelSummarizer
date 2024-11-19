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


def write_building_data_to_csv(data, csv_file_path):
    """
    Write all collected building data to a structured CSV file.
    """
    with open(csv_file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Subcategory", "Details"])  # Standardized headers

        for category, details in data.items():
            writer.writerow([category])  # Category header
            if isinstance(details, dict):  # Handle dictionaries
                for subcategory, value in details.items():
                    if isinstance(value, dict):  # For nested dictionaries like VAV Boxes per AHU
                        writer.writerow([subcategory, "AHU", "VAV Count"])
                        for ahu_name, count in value.items():
                            writer.writerow(["", ahu_name, count])
                    else:
                        writer.writerow(["", subcategory, value])  # Subcategory and details
            elif isinstance(details, list):  # Handle lists
                for item in details:
                    writer.writerow(["", "", item])
            else:  # Handle single values
                writer.writerow(["", "", details])
            writer.writerow([])  # Blank line between categories
