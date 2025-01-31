import os
from brick_model_summarizer import (
    load_graph_once,
    get_class_tag_summary,
    get_ahu_information,
    get_zone_information,
    get_building_information,
    get_meter_information,
    get_central_plant_information,
    get_vav_boxes_per_ahu,
)


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
    graph = load_graph_once(brick_model_file)

    # Get the individual data components
    ahu_data = get_ahu_information(graph)
    print("ahu_data \n", ahu_data)

    zone_info = get_zone_information(graph)
    print("zone_info \n", zone_info)

    class_tag_sum = get_class_tag_summary(graph)
    print("class_tag_sum \n", class_tag_sum)

    building_data = get_building_information(graph)
    print("building_data \n", building_data)

    meter_data = get_meter_information(graph)
    print("meter_data \n", meter_data)

    central_plant_data = get_central_plant_information(graph)
    print("central_plant_data \n", central_plant_data)

    vav_boxes_per_ahu = get_vav_boxes_per_ahu(graph)
    print("vav_boxes_per_ahu \n", vav_boxes_per_ahu)

    expected_hvac_system_counts = {
        "total_variable_air_volume_boxes": 59,
        "water_pump": 4,
        "hot_water_system": 1,
        "hvac_equipment_count": 9,
    }

    # Extract relevant data from individual function outputs
    actual_hvac_system_counts = {
        "total_variable_air_volume_boxes": zone_info.get(
            "total_variable_air_volume_boxes", 0
        ),
        "water_pump": central_plant_data.get("water_pump", 0),
        "hot_water_system": central_plant_data.get("hot_water_system", 0),
        "hvac_equipment_count": building_data.get("hvac_equipment_count", 0),
    }

    print(f"Expected: {expected_hvac_system_counts}")
    print(f"Actual: {actual_hvac_system_counts}")

    print("=======================================")

    assert (
        actual_hvac_system_counts == expected_hvac_system_counts
    ), f"Mismatch in HVAC system counts. Expected: {expected_hvac_system_counts}, Actual: {actual_hvac_system_counts}"
