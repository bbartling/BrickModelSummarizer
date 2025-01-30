import os
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

# pytest -s tests/test_bldg6_ttl.py::test_hvac_system_counts
# pytest -s


def get_brick_model_file():
    """Construct and verify the path to the BRICK model file."""
    relative_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "sample_brick_models",
        "diggs.ttl",
    )
    brick_model_file = os.path.abspath(os.path.normpath(relative_path))

    if not os.path.exists(brick_model_file):
        raise FileNotFoundError(f"BRICK model file not found: {brick_model_file}")

    return brick_model_file


def test_hvac_system_counts():
    """Test to verify counts of VAV boxes, water pumps, hot water systems, and general HVAC system count."""
    brick_model_file = get_brick_model_file()

    # Load the RDF graph once
    graph = load_graph(brick_model_file)

    # Get the individual data components
    ahu_data = collect_ahu_data(identify_ahu_equipment(graph))
    zone_info = identify_zone_equipment(graph)
    zone_data = collect_zone_data(zone_info)
    building_data = collect_building_data(graph)
    meter_data = collect_meter_data(query_meters(graph))
    central_plant_data = collect_central_plant_data(
        identify_hvac_system_equipment(graph)
    )
    vav_boxes_per_ahu = zone_info.get("vav_per_ahu", {})

    expected_hvac_system_counts = {
        "total_variable_air_volume_boxes": 59,
        "water_pump": 4,
        "hot_water_system": 1,
        "hvac_equipment_count": 9,
    }

    # Extract relevant data from individual function outputs
    actual_hvac_system_counts = {
        "total_variable_air_volume_boxes": zone_data.get(
            "total_variable_air_volume_boxes", 0
        ),
        "water_pump": central_plant_data.get("water_pump", 0),
        "hot_water_system": central_plant_data.get("hot_water_system", 0),
        "hvac_equipment_count": building_data.get("hvac_equipment_count", 0),
    }

    print(f"Expected: {expected_hvac_system_counts}")
    print(f"Actual: {actual_hvac_system_counts}")

    assert (
        actual_hvac_system_counts == expected_hvac_system_counts
    ), f"Mismatch in HVAC system counts. Expected: {expected_hvac_system_counts}, Actual: {actual_hvac_system_counts}"
