from brick_model_summarizer.utils import BRICK


def identify_zone_equipment(graph):
    """Combine results from separate queries into a single zone equipment dictionary."""
    zone_equipment = {}
    zone_equipment["zone_setpoints"] = query_zone_setpoints(graph)
    zone_equipment["vav_count"] = count_vav_boxes(graph)
    zone_equipment["vav_per_ahu"] = count_vav_boxes_per_ahu(graph)
    zone_equipment["vav_features"] = count_vav_features(graph)
    zone_equipment["zone_counts"] = count_zone_features(graph)
    return zone_equipment


def query_zone_setpoints(graph):
    """Identify zone setpoints relevant to ASO strategies."""
    zone_setpoints = []
    setpoint_query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?zone ?point WHERE {
        ?zone a brick:Zone .
        ?zone brick:hasPoint ?point .
        ?point a brick:Zone_Air_Temperature_Setpoint .
    }
    """
    results = graph.query(setpoint_query)
    for row in results:
        zone_setpoints.append(str(row.point))
    return zone_setpoints


def count_vav_boxes(graph):
    """Count the total number of VAV boxes (including reheat) in the building model."""
    vav_count = 0
    rvav_count = 0

    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(?vav) AS ?vav_count) (COUNT(?rvav) AS ?rvav_count) WHERE {
        { ?vav a brick:Variable_Air_Volume_Box . }
        UNION
        { ?rvav a brick:Variable_Air_Volume_Box_With_Reheat . }
    }
    """
    results = graph.query(query)
    for row in results:
        vav_count = int(row["vav_count"])
        rvav_count = int(row["rvav_count"])
    return {"vav_count": vav_count, "rvav_count": rvav_count}


def count_vav_boxes_per_ahu(graph):
    """Count the number of VAV boxes associated with each AHU."""
    vav_per_ahu = {}

    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?ahu ?vav_type (COUNT(?vav) AS ?vav_count) WHERE {
        ?ahu a brick:Air_Handling_Unit .
        ?vav a ?vav_type .
        ?vav brick:isPartOf ?ahu .
        FILTER(?vav_type IN (brick:Variable_Air_Volume_Box, brick:Variable_Air_Volume_Box_With_Reheat))
    } GROUP BY ?ahu ?vav_type
    """
    results = graph.query(query)
    for row in results:
        ahu_name = str(row.ahu).split("#")[-1]
        vav_type = str(row.vav_type).split("#")[-1]
        vav_count = int(row.vav_count)
        if ahu_name not in vav_per_ahu:
            vav_per_ahu[ahu_name] = {
                "Variable_Air_Volume_Box": 0,
                "Variable_Air_Volume_Box_With_Reheat": 0,
            }
        vav_per_ahu[ahu_name][vav_type] = vav_count

    return vav_per_ahu


def count_vav_features(graph):
    """Count VAV boxes with specific features."""
    features = {
        "reheat_count": 0,
        "airflow_count": 0,
        "supply_air_temp_count": 0,
        "airflow_setpoint_count": 0,
    }

    feature_points = {
        "reheat_count": ["zone_reheat_valve_command"],
        "airflow_count": ["zone_supply_air_flow"],
        "supply_air_temp_count": ["zone_supply_air_temp"],
        "airflow_setpoint_count": ["zone_supply_air_flow_setpoint"],
    }

    for feature, identifiers in feature_points.items():
        for identifier in identifiers:
            query = f"""
            PREFIX brick: <https://brickschema.org/schema/Brick#>
            SELECT (COUNT(DISTINCT ?vav) AS ?count) WHERE {{
                ?vav a ?vav_type ;
                     brick:hasPoint ?point .
                ?point a brick:Point .
                FILTER(
                    ?vav_type IN (brick:Variable_Air_Volume_Box, brick:Variable_Air_Volume_Box_With_Reheat) &&
                    CONTAINS(LCASE(STR(?point)), "{identifier.lower()}")
                )
            }}
            """
            results = graph.query(query)
            for row in results:
                features[feature] += int(row["count"])

    return features


def count_zone_features(graph):
    """Count additional zone-level features."""
    features = {
        "co2_sensor_count": 0,
        "co2_setpoint_count": 0,
        "zone_air_conditioning_mode_status_count": 0,
        "cooling_temp_setpoint_count": 0,
        "dewpoint_sensor_count": 0,
        "heating_temp_setpoint_count": 0,
        "humidity_sensor_count": 0,
        "humidity_setpoint_count": 0,
        "temperature_sensor_count": 0,
        "temperature_setpoint_count": 0,
        "zone_count": 0,
        "reheat_command_count": 0,
        "reheat_hot_water_system_count": 0,
        "reheat_valve_count": 0,
    }

    feature_classes = {
        "co2_sensor_count": "CO2_Sensor",
        "co2_setpoint_count": "CO2_Setpoint",
        "zone_air_conditioning_mode_status_count": "Zone_Air_Conditioning_Mode_Status",
        "cooling_temp_setpoint_count": "Zone_Air_Cooling_Temperature_Setpoint",
        "dewpoint_sensor_count": "Zone_Air_Dewpoint_Sensor",
        "heating_temp_setpoint_count": "Zone_Air_Heating_Temperature_Setpoint",
        "humidity_sensor_count": "Zone_Air_Humidity_Sensor",
        "humidity_setpoint_count": "Zone_Air_Humidity_Setpoint",
        "temperature_sensor_count": "Zone_Air_Temperature_Sensor",
        "temperature_setpoint_count": "Zone_Air_Temperature_Setpoint",
        "zone_count": "Zone",
        "reheat_command_count": "Reheat_Command",
        "reheat_hot_water_system_count": "Reheat_Hot_Water_System",
        "reheat_valve_count": "Reheat_Valve",
    }

    for feature, brick_class in feature_classes.items():
        query = f"""
        PREFIX brick: <https://brickschema.org/schema/Brick#>
        SELECT (COUNT(?entity) AS ?count) WHERE {{
            ?entity a brick:{brick_class} .
        }}
        """
        results = graph.query(query)
        for row in results:
            features[feature] = int(row["count"])

    return features


def collect_zone_data(zone_info):
    """
    Collect zone information as structured JSON-compatible data.
    """
    zone_data = {}

    # Zone Air Temperature Setpoints
    zone_setpoints = zone_info.get("zone_setpoints", [])
    zone_data["zone_air_temperature_setpoints_found"] = bool(zone_setpoints)

    # Total VAV Boxes
    vav_counts = zone_info.get("vav_count", {})
    zone_data["total_variable_air_volume_boxes"] = vav_counts.get("vav_count", 0)
    zone_data["total_variable_air_volume_boxes_with_reheat"] = vav_counts.get(
        "rvav_count", 0
    )

    # Number of VAV Boxes per AHU
    vav_per_ahu = zone_info.get("vav_per_ahu", {})
    zone_data["number_of_vav_boxes_per_ahu"] = {
        ahu_name.lower(): counts for ahu_name, counts in vav_per_ahu.items()
    }

    # VAV Box Features
    vav_features = zone_info.get("vav_features", {})
    vav_feature_details = {
        "vav_boxes_with_reheat_valve_command": vav_features.get("reheat_count", 0),
        "vav_boxes_with_air_flow_sensors": vav_features.get("airflow_count", 0),
        "vav_boxes_with_supply_air_temp_sensors": vav_features.get(
            "supply_air_temp_count", 0
        ),
        "vav_boxes_with_air_flow_setpoints": vav_features.get(
            "airflow_setpoint_count", 0
        ),
    }
    zone_data.update(vav_feature_details)

    # Additional Zone-Level Features
    zone_features = zone_info.get("zone_counts", {})
    zone_data.update(zone_features)

    return zone_data
