
from rdflib import Namespace
from utils import load_graph

# Define namespaces
BRICK = Namespace("https://brickschema.org/schema/Brick#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

def extract_timeseries_references(graph):
    """
    Extract timeseries references from the Brick model.
    """
    references = []
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?sensor ?label ?timeseries_id WHERE {
        ?sensor brick:timeseries ?timeseries .
        ?sensor rdfs:label ?label .
        ?timeseries brick:hasTimeseriesId ?timeseries_id .
    }
    """
    results = graph.query(query)
    for row in results:
        references.append({
            "sensor": str(row.sensor).split("#")[-1],
            "label": str(row.label),
            "timeseries_id": str(row.timeseries_id)
        })
    return references
