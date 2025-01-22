import os
from brick_model_summarizer.main import process_brick_file


def get_brick_model_file():
    """Construct and verify the path to the BRICK model file."""
    relative_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "sample_brick_models",
        "bldg6.ttl",
    )
    brick_model_file = os.path.abspath(os.path.normpath(relative_path))

    if not os.path.exists(brick_model_file):
        raise FileNotFoundError(f"BRICK model file not found: {brick_model_file}")

    return brick_model_file


def test_ahu_information():
    brick_model_file = get_brick_model_file()
    building_data = process_brick_file(brick_model_file)

    expected_ahu_info = {
        "total_ahus": 16,
        "constant_volume_ahus": 11,
        "variable_air_volume_ahus": 0,
        "ahus_with_cooling_coil": 10,
        "ahus_with_heating_coil": 7,
        "ahus_with_dx_staged_cooling": 0,
        "ahus_with_return_fans": 0,
        "ahus_with_supply_fans": 0,
        "ahus_with_return_air_temp_sensors": 4,
        "ahus_with_mixing_air_temp_sensors": 1,
        "ahus_with_leaving_air_temp_sensors": 18,
        "ahus_with_leaving_air_temp_setpoint": 9,
        "ahus_with_duct_pressure_setpoint": 0,
        "ahus_with_duct_pressure": 0,
    }
    assert building_data["ahu_information"] == expected_ahu_info


def test_zone_information():
    brick_model_file = get_brick_model_file()
    building_data = process_brick_file(brick_model_file)

    expected_zone_info = {
        "zone_air_temperature_setpoints_found": True,
        "total_vav_boxes": 132,
        "number_of_vav_boxes_per_ahu": {
            "ah1s": 4,
            "ah2n": 3,
            "ah2s": 3,
            "ah3s": 1,
            "ahbs": 2,
            "ahu01n": 24,
            "ahu01s": 22,
            "ahu02n": 10,
            "ahu02s": 30,
            "ahu03n": 14,
            "ahu03s": 30,
        },
        "vav_boxes_with_reheat_valve_command": 0,
        "vav_boxes_with_air_flow_sensors": 0,
        "vav_boxes_with_supply_air_temp_sensors": 0,
        "vav_boxes_with_air_flow_setpoints": 0,
        "cooling_only_vav_boxes": 132,
    }
    assert building_data["zone_information"] == expected_zone_info


def test_building_information():
    brick_model_file = get_brick_model_file()
    building_data = process_brick_file(brick_model_file)

    expected_building_info = {
        "building_area": "130149 sq ft",
        "number_of_floors": 4,
    }
    assert building_data["building_information"] == expected_building_info


def test_meter_information():
    brick_model_file = get_brick_model_file()
    building_data = process_brick_file(brick_model_file)

    expected_meter_info = {
        "btu_meter_present": False,
        "electrical_meter_present": False,
        "water_meter_present": False,
        "gas_meter_present": False,
        "pv_meter_present": False,
    }
    assert building_data["meter_information"] == expected_meter_info


def test_central_plant_information():
    brick_model_file = get_brick_model_file()
    building_data = process_brick_file(brick_model_file)

    expected_central_plant_info = {
        "total_chillers": 1,
        "total_boilers": 0,
        "total_cooling_towers": 0,
        "chillers_with_water_flow": 0,
        "boilers_with_water_flow": 0,
        "cooling_towers_with_fan": 0,
        "cooling_towers_with_temp_sensors": 0,
    }
    assert building_data["central_plant_information"] == expected_central_plant_info
