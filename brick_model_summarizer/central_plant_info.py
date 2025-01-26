from brick_model_summarizer.utils import BRICK


def identify_hvac_system_equipment(graph):
    """Combine results from separate queries into a single dictionary for HVAC equipment."""
    hvac_equipment = {}
    hvac_equipment["hvac_system_counts"] = count_hvac_systems(graph)
    hvac_equipment["hvac_features"] = count_hvac_features(graph)
    return hvac_equipment


def count_hvac_systems(graph):
    """Count the total number of chillers, boilers, cooling towers, heat exchangers, hot water systems, and water pumps in the building model."""
    counts = {
        "chiller_count": 0,
        "water_cooled_chiller_count": 0,
        "air_cooled_chiller_count": 0,
        "centrifugal_chiller_count": 0,
        "absorption_chiller_count": 0,
        "boiler_count": 0,
        "natural_gas_boiler_count": 0,
        "noncondensing_natural_gas_boiler_count": 0,
        "condensing_natural_gas_boiler_count": 0,
        "electric_boiler_count": 0,
        "cooling_tower_count": 0,
        "cooling_tower_fan_count": 0,
        "heat_exchanger_count": 0,
        "heat_exchanger_discharge_temp_sensor_count": 0,
        "heat_exchanger_leaving_temp_sensor_count": 0,
        "heat_exchanger_supply_temp_sensor_count": 0,
        "heat_exchanger_system_enable_status_count": 0,
        "heat_pump_air_source_condensing_unit_count": 0,
        "heat_pump_condensing_unit_count": 0,
        "heat_pump_ground_source_condensing_unit_count": 0,
        "heat_pump_water_source_condensing_unit_count": 0,
        "heat_recovery_air_source_condensing_unit_count": 0,
        "heat_recovery_condensing_unit_count": 0,
        "heat_recovery_hot_water_system_count": 0,
        "heat_recovery_water_source_condensing_unit_count": 0,
        "hot_water_system_count": 0,
        "water_pump_count": 0,
        "chilled_water_system_count": 0,
        "condenser_water_loop_count": 0,
        "condenser_water_pump_count": 0,
        "condenser_water_system_count": 0,
        "domestic_hot_water_system_count": 0,
        "preheat_hot_water_system_count": 0,
        "radiation_hot_water_system_count": 0,
        "reheat_hot_water_system_count": 0,
        "water_system_count": 0,
    }
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?type (COUNT(?equip) AS ?count) WHERE {
        ?equip a ?type .
        FILTER(?type IN (
            brick:Chiller,
            brick:Water_Cooled_Chiller,
            brick:Air_Cooled_Chiller,
            brick:Centrifugal_Chiller,
            brick:Absorption_Chiller,
            brick:Boiler,
            brick:Natural_Gas_Boiler,
            brick:Noncondensing_Natural_Gas_Boiler,
            brick:Condensing_Natural_Gas_Boiler,
            brick:Electric_Boiler,
            brick:Cooling_Tower,
            brick:Cooling_Tower_Fan,
            brick:Heat_Exchanger,
            brick:Heat_Exchanger_Discharge_Water_Temperature_Sensor,
            brick:Heat_Exchanger_Leaving_Water_Temperature_Sensor,
            brick:Heat_Exchanger_Supply_Water_Temperature_Sensor,
            brick:Heat_Exchanger_System_Enable_Status,
            brick:Heat_Pump_Air_Source_Condensing_Unit,
            brick:Heat_Pump_Condensing_Unit,
            brick:Heat_Pump_Ground_Source_Condensing_Unit,
            brick:Heat_Pump_Water_Source_Condensing_Unit,
            brick:Heat_Recovery_Air_Source_Condensing_Unit,
            brick:Heat_Recovery_Condensing_Unit,
            brick:Heat_Recovery_Hot_Water_System,
            brick:Heat_Recovery_Water_Source_Condensing_Unit,
            brick:Hot_Water_System,
            brick:Water_Pump,
            brick:Chilled_Water_System,
            brick:Condenser_Water_Loop,
            brick:Condenser_Water_Pump,
            brick:Condenser_Water_System,
            brick:Domestic_Hot_Water_System,
            brick:Preheat_Hot_Water_System,
            brick:Radiation_Hot_Water_System,
            brick:Reheat_Hot_Water_System,
            brick:Water_System
        ))
    } GROUP BY ?type
    """
    results = graph.query(query)
    for row in results:
        equip_type = str(row.type)
        count = int(row["count"])
        counts[equip_type.split("#")[-1].lower()] = count
    return counts


def count_hvac_features(graph):
    """Count specific features for chillers, boilers, cooling towers, heat exchangers, hot water systems, water pumps, and other systems."""
    features = {
        "chiller_water_flow_count": 0,
        "boiler_water_flow_count": 0,
        "cooling_tower_fan_count": 0,
        "cooling_tower_temp_count": 0,
        "heat_exchanger_discharge_temp_sensor_count": 0,
        "heat_exchanger_leaving_temp_sensor_count": 0,
        "heat_exchanger_supply_temp_sensor_count": 0,
        "heat_exchanger_system_enable_status_count": 0,
    }
    feature_queries = {
        "chiller_water_flow_count": """
        PREFIX brick: <https://brickschema.org/schema/Brick#>
        SELECT (COUNT(?point) AS ?count) WHERE {
            ?equip a brick:Chiller ;
                   brick:hasPoint ?point .
            ?point a brick:Water_Flow_Sensor .
        }
        """,
        "boiler_water_flow_count": """
        PREFIX brick: <https://brickschema.org/schema/Brick#>
        SELECT (COUNT(?point) AS ?count) WHERE {
            ?equip a brick:Boiler ;
                   brick:hasPoint ?point .
            ?point a brick:Water_Flow_Sensor .
        }
        """,
        # Add additional queries for each feature if needed
    }

    for feature, query in feature_queries.items():
        results = graph.query(query)
        for row in results:
            features[feature] = int(row["count"])

    return features


def collect_central_plant_data(hvac_info):
    """Collect central plant equipment information as structured JSON-compatible data."""
    central_plant_data = {}

    # Collect central plant counts
    hvac_counts = hvac_info.get("hvac_system_counts", {})
    for key, value in hvac_counts.items():
        central_plant_data[key] = value

    # Collect central plant features
    hvac_features = hvac_info.get("hvac_features", {})
    for key, value in hvac_features.items():
        central_plant_data[key] = value

    return central_plant_data
