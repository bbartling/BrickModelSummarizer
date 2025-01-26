from brick_model_summarizer.utils import load_graph
from brick_model_summarizer.ahu_info import identify_ahu_equipment, collect_ahu_data
from brick_model_summarizer.zone_info import identify_zone_equipment, collect_zone_data
from brick_model_summarizer.meters_info import query_meters, collect_meter_data
from brick_model_summarizer.central_plant_info import (
    identify_hvac_system_equipment,
    collect_central_plant_data,
)
from brick_model_summarizer.building_info import collect_building_data
from brick_model_summarizer.class_tag_checker import analyze_classes_and_tags


def process_brick_file(brick_model_file):
    """Process a single TTL file and return building data."""
    print(f"Processing BRICK model file: {brick_model_file}")

    # Load the RDF graph
    graph = load_graph(brick_model_file)

    # Custom class and tag analysis
    class_tag_summary = analyze_classes_and_tags(graph)

    # Collect data from different modules
    ahu_data = collect_ahu_data(identify_ahu_equipment(graph))
    zone_info = identify_zone_equipment(graph)
    zone_data = collect_zone_data(zone_info)
    building_data = collect_building_data(graph)
    meter_data = collect_meter_data(query_meters(graph))
    central_plant_data = collect_central_plant_data(
        identify_hvac_system_equipment(graph)
    )
    vav_boxes_per_ahu = zone_info.get("vav_per_ahu", {})

    # Construct the complete data dictionary with lowercase keys
    complete_data = {
        "ahu_information": ahu_data,
        "zone_information": zone_data,
        "building_information": building_data,
        "meter_information": meter_data,
        "central_plant_information": central_plant_data,
        "number_of_vav_boxes_per_ahu": vav_boxes_per_ahu,
        "class_tag_summary": class_tag_summary,
    }

    print("\n=== Building Summary ===")
    print(complete_data)

    return complete_data
