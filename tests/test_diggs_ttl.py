import os
from brick_model_summarizer.main import process_brick_file

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
    building_data = process_brick_file(brick_model_file)

    expected_hvac_system_counts = {
        "total_variable_air_volume_boxes": 59,
        "water_pump": 4,
        "hot_water_system": 1,
        "hvac_equipment_count": 9,
    }

    # Extract relevant data from the building summary
    actual_hvac_system_counts = {
        "total_variable_air_volume_boxes": building_data["zone_information"].get(
            "total_variable_air_volume_boxes", 0
        ),
        "water_pump": building_data["central_plant_information"].get("water_pump", 0),
        "hot_water_system": building_data["central_plant_information"].get(
            "hot_water_system", 0
        ),
        "hvac_equipment_count": building_data["building_information"].get(
            "hvac_equipment_count", 0
        ),
    }

    assert (
        actual_hvac_system_counts == expected_hvac_system_counts
    ), f"Mismatch in HVAC system counts. Expected: {expected_hvac_system_counts}, Actual: {actual_hvac_system_counts}"
