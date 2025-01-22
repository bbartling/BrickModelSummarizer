# BRICK Model Summarizer

[![PyPI version](https://badge.fury.io/py/brick-model-summarizer.svg)](https://pypi.org/project/brick-model-summarizer/)
[![Tests](https://github.com/bbartling/BrickModelSummarizer/actions/workflows/tests.yml/badge.svg)](https://github.com/bbartling/BrickModelSummarizer/actions)


**BRICK Model Summarizer** is a Python tool designed to validate and benchmark AI-generated BRICK models against reference models. It transforms complex BRICK schema TTL files into concise, human-readable summaries of HVAC systems, zones, meters, and central plants. By leveraging [reference BRICK models](https://brickschema.org/resources/#reference-brick-models), this tool enables users to validate AI-created models for consistency, accuracy, and adherence to expected standards.

## Purpose

The primary purpose of this repository is to provide a framework for summarizing BRICK models into HVAC-centric insights. This is especially useful for:
- **Benchmarking AI-generated BRICK models** against reference models.
- **Validating BRICK schemas** for completeness and alignment with building system expectations.
- **Empowering building engineers, analysts, and AI developers** with clear summaries of mechanical systems and operational data.

## Key Features

- **HVAC-Focused Summarization**: Extracts key details about AHUs, VAVs, meters, and central plant equipment.
- **Model Validation**: Provides a framework for benchmarking AI-created BRICK models.
- **Scalable Processing**: Processes individual or multiple BRICK schema TTL files.


## Installation
```bash
pip install brick-model-summarizer
```

### Local Installation for development purposes

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bbartling/brick-model-summarizer.git
   cd brick-model-summarizer
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   ```

3. **Install the package locally**:
   ```bash
   pip install .
   ```

---

## Usage

The package includes functions for summarizing BRICK models and generating detailed outputs. Below is an example of how to use the tool in Python to generate JSON-style data.


### Example: Processing a BRICK Model

```python
from brick_model_summarizer.main import process_brick_file
import json

# Path to the BRICK schema TTL file
brick_model_file = "sample_brick_models/bldg6.ttl"

# Generate a summary
building_data = process_brick_file(brick_model_file)

# Print the output in JSON format
print(json.dumps(building_data, indent=2))

# Optionally, save the output as a JSON file
output_file = "bldg6_summary.json"
with open(output_file, 'w') as file:
    json.dump(building_data, file, indent=2)
```

### Example Output

```json
{
  "ahu_information": {
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
    "ahus_with_duct_pressure": 0
  },
  "zone_information": {
    "zone_air_temperature_setpoints_found": true,
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
      "ahu03s": 30
    },
    "vav_boxes_with_reheat_valve_command": 0,
    "vav_boxes_with_air_flow_sensors": 0,
    "vav_boxes_with_supply_air_temp_sensors": 0,
    "vav_boxes_with_air_flow_setpoints": 0,
    "cooling_only_vav_boxes": 132
  },
  "building_information": {
    "building_area": "130149 sq ft",
    "number_of_floors": 4
  },
  "meter_information": {
    "btu_meter_present": false,
    "electrical_meter_present": false,
    "water_meter_present": false,
    "gas_meter_present": false,
    "pv_meter_present": false
  },
  "central_plant_information": {
    "total_chillers": 1,
    "total_boilers": 0,
    "total_cooling_towers": 0,
    "chillers_with_water_flow": 0,
    "boilers_with_water_flow": 0,
    "cooling_towers_with_fan": 0,
    "cooling_towers_with_temp_sensors": 0
  }
}
```

---


### Validating AI-Generated Models
Use the outputs to compare AI-created models against reference BRICK models, checking for consistency in:
- Equipment classification (e.g., AHUs, VAVs).
- Sensor and control points.
- Central plant configurations.

## Sample Data

Reference BRICK models from [BRICK resources](https://brickschema.org/resources/#reference-brick-models) are included in the `sample_brick_models` directory. These files can be used for testing and validation.

## Web App Demo
View a web app interface on Bens Pythonanywhere account for free!

* https://bensapi.pythonanywhere.com/
* Upload and process `.ttl` files to generate detailed BRICK model summaries.
* Compare your AI-generated models with [official BRICK Reference Models](https://brickschema.org/resources/#reference-brick-models).
* Easy-to-use web interface with support for `.ttl` file validation.

![BRICK Model Summarizer Interface](https://github.com/bbartling/BrickModelSummarizer/blob/develop/flask_app/app_interface.png?raw=true)

## Contributing

We welcome contributions to improve the repository. Please submit issues or pull requests to discuss new features, bug fixes, or enhancements.

## Roadmap

### Planned Enhancements
- **ECM and KPI Suggestions**: Develop functionality to recommend energy conservation measures (ECMs) based on model summaries.
- **Advanced Validation**: Add checks for missing or inconsistent relationships in AI-generated models.
- **PyPI Distribution**: Prepare the package for publication on PyPI.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
