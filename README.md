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
Tested in Linux and Windows Subsystem for Linux
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
   source env/bin/activate
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

# Get the absolute path of the project root
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Construct the relative path to the BRICK model
brick_model_path = os.path.join(project_root, "sample_brick_models", "diggs.ttl")

print("Resolved Brick Model Path:", brick_model_path)

# Load the RDF graph once
graph = load_graph_once(brick_model_path)

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

```

### Example Output

```python
=== AHU DEBUG Summary ===
Processed AHU's: 0

ahu_data
 {'total_ahus': 0, 'constant_volume_ahus': 0, 'variable_air_volume_ahus': 0, 'ahus_with_cooling_coil': 0, 'ahus_with_heating_coil': 0, 'ahus_with_return_fans': 0, 'ahus_with_supply_fans': 0, 'ahus_with_return_air_temp_sensors': 0, 'ahus_with_mixing_air_temp_sensors': 0, 'ahus_with_supply_air_temp_sensors': 0, 'ahus_with_supply_air_temp_setpoints': 0, 'ahus_with_static_pressure_sensors': 0, 'ahus_with_static_pressure_setpoints': 0, 'ahus_with_air_flow_sensors': 0, 'ahus_with_air_flow_setpoints': 0, 'ahus_with_active_chilled_beams': 0, 'ahus_with_chilled_beams': 0, 'ahus_with_passive_chilled_beams': 0, 'ahus_with_heat_wheels': 0, 'ahus_with_heat_wheel_vfds': 0}
zone_info 
 {'zone_air_temperature_setpoints_found': False, 'total_variable_air_volume_boxes': 59, 'total_variable_air_volume_boxes_with_reheat': 0, 'number_of_vav_boxes_per_ahu': {}, 'vav_boxes_with_reheat_valve_command': 0, 'vav_boxes_with_air_flow_sensors': 0, 'vav_boxes_with_supply_air_temp_sensors': 0, 'vav_boxes_with_air_flow_setpoints': 0, 'co2_sensor_count': 0, 'co2_setpoint_count': 0, 'zone_air_conditioning_mode_status_count': 0, 'cooling_temp_setpoint_count': 0, 'dewpoint_sensor_count': 0, 'heating_temp_setpoint_count': 0, 'humidity_sensor_count': 0, 'humidity_setpoint_count': 0, 'temperature_sensor_count': 0, 'temperature_setpoint_count': 0, 'zone_count': 0, 'reheat_command_count': 0, 'reheat_hot_water_system_count': 0, 'reheat_valve_count': 0}

Class Similarities:
class_tag_sum
 {'class_mismatches': [], 'tag_mismatches': []}
building_data 
 {'building_area': 'not_available', 'number_of_floors': 'not_available', 'hvac_equipment_count': 9, 'hvac_zone_count': 0}
meter_data 
 {'chilled_water_meter_present': False, 'hot_water_meter_present': False, 'building_electrical_meter_present': False, 'building_gas_meter_present': False, 'building_water_meter_present': False, 'electric_energy_sensor_count': 0, 'electric_power_sensor_count': 0, 'active_power_sensor_count': 0, 'ev_charging_hub_count': 0, 'ev_charging_port_count': 0, 'ev_charging_station_count': 0, 'electrical_energy_usage_sensor_count': 0, 'pv_generation_system_count': 0, 'pv_panel_count': 0, 'photovoltaic_array_count': 0, 'photovoltaic_current_output_sensor_count': 0, 'photovoltaic_inverter_count': 0, 'peak_demand_sensor_count': 0, 'people_count_sensor_count': 0}
central_plant_data 
 {'chiller_count': 0, 'water_cooled_chiller_count': 0, 'air_cooled_chiller_count': 0, 'centrifugal_chiller_count': 0, 'absorption_chiller_count': 0, 'boiler_count': 0, 'natural_gas_boiler_count': 0, 'noncondensing_natural_gas_boiler_count': 0, 'condensing_natural_gas_boiler_count': 0, 'electric_boiler_count': 0, 'cooling_tower_count': 0, 'cooling_tower_fan_count': 0, 'heat_exchanger_count': 0, 'heat_exchanger_discharge_temp_sensor_count': 0, 'heat_exchanger_leaving_temp_sensor_count': 0, 'heat_exchanger_supply_temp_sensor_count': 0, 'heat_exchanger_system_enable_status_count': 0, 'heat_pump_air_source_condensing_unit_count': 0, 'heat_pump_condensing_unit_count': 0, 'heat_pump_ground_source_condensing_unit_count': 0, 'heat_pump_water_source_condensing_unit_count': 0, 'heat_recovery_air_source_condensing_unit_count': 0, 'heat_recovery_condensing_unit_count': 0, 'heat_recovery_hot_water_system_count': 0, 'heat_recovery_water_source_condensing_unit_count': 0, 'hot_water_system_count': 0, 'water_pump_count': 0, 'chilled_water_system_count': 0, 'condenser_water_loop_count': 0, 'condenser_water_pump_count': 0, 'condenser_water_system_count': 0, 'domestic_hot_water_system_count': 0, 'preheat_hot_water_system_count': 0, 'radiation_hot_water_system_count': 0, 'reheat_hot_water_system_count': 0, 'water_system_count': 0, 'water_system': 1, 'water_pump': 4, 'hot_water_system': 1, 'chiller_water_flow_count': 0, 'boiler_water_flow_count': 0, 'cooling_tower_temp_count': 0}
vav_boxes_per_ahu 
 {}
```

One note on the output of the  `Class Similarities` is it finds mismatched BRICK classes and tags by comparing them to the most current standard. If a mismatch is found, it returns a dictionary like data in the format of `('custom_tag', 'standard_tag', 0.90)`:  

```python
{
    'class_mismatches': [('Air_Handler_Unit', 'Air_Handling_Unit', 0.85)],
    'tag_mismatches': [('custom_tag', 'standard_tag', 0.90)]
}
```
Here, **0.85 and 0.90** are similarity scores from `SequenceMatcher`, which measure how close the custom class or tag is to the standard one. These values provide a **statistical similarity percentage** from the Python `difflib` package, helping you assess how much a custom class deviates from the standard. 
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
