import os
from brick_model_summarizer.main import process_brick_file


def test_process_brick_file():
    """Test the processing of a BRICK model file."""

    # Construct the relative path and resolve it to an absolute path
    relative_path = os.path.join(
        os.path.dirname(__file__),  # Directory of the current script
        "..",  # Go up one level to the project root
        "sample_brick_models",  # Subdirectory for Brick models
        "bldg6.ttl",  # The Brick model file
    )
    brick_model_file = os.path.abspath(os.path.normpath(relative_path))

    # Verify the constructed path
    print(f"Using BRICK model file: {brick_model_file}")

    # Check if the file exists
    if not os.path.exists(brick_model_file):
        raise FileNotFoundError(f"BRICK model file not found: {brick_model_file}")

    # brick_model_file = r"C:\Users\ben\Documents\HvacGPT\sample_brick_models\bldg6.ttl"

    # Process the BRICK model file
    building_data = process_brick_file(brick_model_file)

    # Expected results
    expected_ahu_info = {
        "Total AHUs": 16,
        "Constant Volume AHUs": 11,
        "Variable Air Volume AHUs": 0,
        "AHUs with Cooling Coil": 10,
        "AHUs with Heating Coil": 7,
        "AHUs with DX Staged Cooling": 0,
        "AHUs with Return Fans": 0,
        "AHUs with Supply Fans": 0,
        "AHUs with Return Air Temp Sensors": 4,
        "AHUs with Mixing Air Temp Sensors": 1,
        "AHUs with Leaving Air Temp Sensors": 18,
        "AHUs with Leaving Air Temp Setpoint": 9,
        "AHUs with Duct Pressure Setpoint": 0,
        "AHUs with Duct Pressure": 0,
    }

    expected_zone_info = {
        "Zone Air Temperature Setpoints": "Zone Air Temperature Setpoints Found.",
        "Total VAV Boxes": 132,
        "Number of VAV Boxes per AHU": {
            "AHU: AH1S": 4,
            "AHU: AH2N": 3,
            "AHU: AH2S": 3,
            "AHU: AH3S": 1,
            "AHU: AHBS": 2,
            "AHU: AHU01N": 24,
            "AHU: AHU01S": 22,
            "AHU: AHU02N": 10,
            "AHU: AHU02S": 30,
            "AHU: AHU03N": 14,
            "AHU: AHU03S": 30,
        },
        "VAV Boxes with Reheat Valve Command": 0,
        "VAV Boxes with Air Flow Sensors": 0,
        "VAV Boxes with Supply Air Temp Sensors": 0,
        "VAV Boxes with Air Flow Setpoints": 0,
        "Cooling Only VAV Boxes": 132,
    }

    expected_building_info = {
        "Building Area": "130149 sq ft",
        "Number of Floors": 4,
    }

    expected_meter_info = {
        "BTU Meter Present": False,
        "Electrical Meter Present": False,
        "Water Meter Present": False,
        "Gas Meter Present": False,
        "PV Meter Present": False,
    }

    expected_central_plant_info = {
        "Total Chillers": 1,
        "Total Boilers": 0,
        "Total Cooling Towers": 0,
        "Chillers with Water Flow": 0,
        "Boilers with Water Flow": 0,
        "Cooling Towers with Fan": 0,
        "Cooling Towers with Temp Sensors": 0,
    }

    # Assertions for each section
    assert building_data["AHU Information"] == expected_ahu_info
    assert building_data["Zone Information"] == expected_zone_info
    assert building_data["Building Information"] == expected_building_info
    assert building_data["Meter Information"] == expected_meter_info
    assert building_data["Central Plant Information"] == expected_central_plant_info
