from brick_model_summarizer.utils import load_graph
from brick_model_summarizer.ahu_info import identify_ahu_equipment, collect_ahu_data
from brick_model_summarizer.zone_info import identify_zone_equipment, collect_zone_data
from brick_model_summarizer.meters_info import query_meters, collect_meter_data
from brick_model_summarizer.central_plant_info import (
    identify_hvac_system_equipment,
    collect_central_plant_data,
)
from brick_model_summarizer.building_info import collect_building_data


def process_brick_file(brick_model_file):
    """Process a single TTL file and return building data."""
    print(f"Processing BRICK model file: {brick_model_file}")

    # Load the RDF graph
    graph = load_graph(brick_model_file)

    # Collect building data
    building_data = {
        "AHU Information": collect_ahu_data(identify_ahu_equipment(graph)),
        "Zone Information": collect_zone_data(identify_zone_equipment(graph)),
        "Building Information": collect_building_data(graph),
        "Meter Information": collect_meter_data(query_meters(graph)),
        "Central Plant Information": collect_central_plant_data(
            identify_hvac_system_equipment(graph)
        ),
    }

    # Generate and print the text description
    # description = generate_text_description(building_data, [])
    print("\n=== Building Summary ===")
    print(building_data)

    return building_data
