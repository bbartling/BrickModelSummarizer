from brick_model_summarizer.utils import BRICK, UNIT


def query_meters(graph):
    """Identify and count all meter types and their associations."""
    meters = {
        "chilled_water_meter": False,
        "hot_water_meter": False,
        "building_electrical_meter": False,
        "building_gas_meter": False,
        "building_water_meter": False,
        "electric_energy_sensors": 0,
        "electric_power_sensors": 0,
        "active_power_sensors": 0,
        "ev_charging_hubs": 0,
        "ev_charging_ports": 0,
        "ev_charging_stations": 0,
        "electrical_energy_usage_sensors": 0,
        "pv_generation_systems": 0,
        "pv_panels": 0,
        "photovoltaic_arrays": 0,
        "photovoltaic_current_output_sensors": 0,
        "photovoltaic_inverters": 0,
        "peak_demand_sensors": 0,
        "people_count_sensors": 0,
    }

    # Query for updated meter types and equipment
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?meter ?type WHERE {
        ?meter a ?type .
        FILTER(?type IN (
            brick:Building_Chilled_Water_Meter,
            brick:Building_Hot_Water_Meter,
            brick:Building_Electrical_Meter,
            brick:Building_Gas_Meter,
            brick:Building_Water_Meter,
            brick:Electric_Energy_Sensor,
            brick:Electric_Power_Sensor,
            brick:Active_Power_Sensor,
            brick:Electric_Vehicle_Charging_Hub,
            brick:Electric_Vehicle_Charging_Port,
            brick:Electric_Vehicle_Charging_Station,
            brick:Electrical_Energy_Usage_Sensor,
            brick:PV_Generation_System,
            brick:PV_Panel,
            brick:Photovoltaic_Array,
            brick:Photovoltaic_Current_Output_Sensor,
            brick:Photovoltaic_Inverter,
            brick:Peak_Demand_Sensor,
            brick:People_Count_Sensor_Equipment
        ))
    }
    """
    results = graph.query(query)
    for row in results:
        meter_type = str(row.type).split("#")[-1]
        if meter_type == "Building_Chilled_Water_Meter":
            meters["chilled_water_meter"] = True
        elif meter_type == "Building_Hot_Water_Meter":
            meters["hot_water_meter"] = True
        elif meter_type == "Building_Electrical_Meter":
            meters["building_electrical_meter"] = True
        elif meter_type == "Building_Gas_Meter":
            meters["building_gas_meter"] = True
        elif meter_type == "Building_Water_Meter":
            meters["building_water_meter"] = True
        elif meter_type == "Electric_Energy_Sensor":
            meters["electric_energy_sensors"] += 1
        elif meter_type == "Electric_Power_Sensor":
            meters["electric_power_sensors"] += 1
        elif meter_type == "Active_Power_Sensor":
            meters["active_power_sensors"] += 1
        elif meter_type == "Electric_Vehicle_Charging_Hub":
            meters["ev_charging_hubs"] += 1
        elif meter_type == "Electric_Vehicle_Charging_Port":
            meters["ev_charging_ports"] += 1
        elif meter_type == "Electric_Vehicle_Charging_Station":
            meters["ev_charging_stations"] += 1
        elif meter_type == "Electrical_Energy_Usage_Sensor":
            meters["electrical_energy_usage_sensors"] += 1
        elif meter_type == "PV_Generation_System":
            meters["pv_generation_systems"] += 1
        elif meter_type == "PV_Panel":
            meters["pv_panels"] += 1
        elif meter_type == "Photovoltaic_Array":
            meters["photovoltaic_arrays"] += 1
        elif meter_type == "Photovoltaic_Current_Output_Sensor":
            meters["photovoltaic_current_output_sensors"] += 1
        elif meter_type == "Photovoltaic_Inverter":
            meters["photovoltaic_inverters"] += 1
        elif meter_type == "Peak_Demand_Sensor":
            meters["peak_demand_sensors"] += 1
        elif meter_type == "People_Count_Sensor_Equipment":
            meters["people_count_sensors"] += 1

    return meters


def collect_meter_data(meter_info):
    """
    Collect meter information as structured JSON-compatible data.
    """
    # Prepare meter information with snake_case keys
    meter_data = {
        "chilled_water_meter_present": meter_info.get("chilled_water_meter", "Unknown"),
        "hot_water_meter_present": meter_info.get("hot_water_meter", "Unknown"),
        "building_electrical_meter_present": meter_info.get(
            "building_electrical_meter", "Unknown"
        ),
        "building_gas_meter_present": meter_info.get("building_gas_meter", "Unknown"),
        "building_water_meter_present": meter_info.get(
            "building_water_meter", "Unknown"
        ),
        "electric_energy_sensor_count": meter_info.get("electric_energy_sensors", 0),
        "electric_power_sensor_count": meter_info.get("electric_power_sensors", 0),
        "active_power_sensor_count": meter_info.get("active_power_sensors", 0),
        "ev_charging_hub_count": meter_info.get("ev_charging_hubs", 0),
        "ev_charging_port_count": meter_info.get("ev_charging_ports", 0),
        "ev_charging_station_count": meter_info.get("ev_charging_stations", 0),
        "electrical_energy_usage_sensor_count": meter_info.get(
            "electrical_energy_usage_sensors", 0
        ),
        "pv_generation_system_count": meter_info.get("pv_generation_systems", 0),
        "pv_panel_count": meter_info.get("pv_panels", 0),
        "photovoltaic_array_count": meter_info.get("photovoltaic_arrays", 0),
        "photovoltaic_current_output_sensor_count": meter_info.get(
            "photovoltaic_current_output_sensors", 0
        ),
        "photovoltaic_inverter_count": meter_info.get("photovoltaic_inverters", 0),
        "peak_demand_sensor_count": meter_info.get("peak_demand_sensors", 0),
        "people_count_sensor_count": meter_info.get("people_count_sensors", 0),
    }
    return meter_data
