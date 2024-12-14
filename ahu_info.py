# ahu_info.py
from utils import BRICK


def identify_ahu_equipment(graph):
    """Combine results from separate queries into a single AHU equipment dictionary."""
    ahu_equipment = {}
    ahu_equipment["ahu_count"] = count_ahus(graph)
    ahu_equipment["ahu_types"] = count_ahu_types(graph)
    ahu_equipment["ahu_features"] = count_ahu_features(graph)
    return ahu_equipment


def count_ahus(graph):
    """Count the total number of AHUs in the building model."""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT (COUNT(?ahu) AS ?ahu_count) WHERE {
        ?ahu a ?ahu_type .
        FILTER(?ahu_type IN (brick:Air_Handler_Unit, brick:AHU))
    }
    """
    results = graph.query(query)
    for row in results:
        return int(row.ahu_count)
    return 0


def count_ahu_features(graph):
    """Count AHUs with specific features and classify them as VAV or CV."""
    features = {
        "cv_count": 0,
        "vav_count": 0,
        "cooling_coil_count": 0,
        "heating_coil_count": 0,
        "dx_staged_cooling_count": 0,
        "return_fan_count": 0,
        "supply_fan_count": 0,
        "return_temp_count": 0,
        "mixing_temp_count": 0,
        "leaving_temp_count": 0,
        "leaving_air_temp_setpoint_count": 0,
        "duct_pressure_count": 0,
        "duct_pressure_setpoint_count": 0,
    }

    # Unified query with filters for each feature keyword
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?ahu ?point WHERE {
        ?ahu a brick:Air_Handler_Unit .
        ?ahu brick:hasPoint ?point .
        FILTER(
            CONTAINS(LCASE(STR(?point)), "cooling_valve_output") ||
            CONTAINS(LCASE(STR(?point)), "heating_valve_output") ||
            CONTAINS(LCASE(STR(?point)), "dx_staged_cooling") ||
            CONTAINS(LCASE(STR(?point)), "return_fan") ||
            CONTAINS(LCASE(STR(?point)), "supply_fan") ||
            CONTAINS(LCASE(STR(?point)), "return_air_temp") ||
            CONTAINS(LCASE(STR(?point)), "mixed_air_temp") ||
            CONTAINS(LCASE(STR(?point)), "supply_air_temp") ||
            CONTAINS(LCASE(STR(?point)), "supply_air_temp_setpoint") ||
            CONTAINS(LCASE(STR(?point)), "supply_air_pressure") ||
            CONTAINS(LCASE(STR(?point)), "supply_air_pressure_setpoint")
        )
    }
    """
    ahu_points = {}
    results = graph.query(query)
    for row in results:
        ahu = str(row.ahu)
        point = str(row.point).lower()
        if ahu not in ahu_points:
            ahu_points[ahu] = []

        ahu_points[ahu].append(point)

        # Increment feature counters
        if "cooling_valve_output" in point:
            features["cooling_coil_count"] += 1
        if "heating_valve_output" in point:
            features["heating_coil_count"] += 1
        if "dx_staged_cooling" in point:
            features["dx_staged_cooling_count"] += 1
        if "return_fan" in point:
            features["return_fan_count"] += 1
        if "supply_fan" in point:
            features["supply_fan_count"] += 1
        if "return_air_temp" in point:
            features["return_temp_count"] += 1
        if "mixed_air_temp" in point:
            features["mixing_temp_count"] += 1
        if "supply_air_temp" in point:
            features["leaving_temp_count"] += 1
        if "supply_air_temp_setpoint" in point:
            features["leaving_air_temp_setpoint_count"] += 1
        if "supply_air_pressure_setpoint" in point:
            features["duct_pressure_setpoint_count"] += 1
        if "supply_air_pressure" in point:
            features["duct_pressure_count"] += 1

    # Classify AHUs as VAV or CV based on their points
    for ahu, points in ahu_points.items():
        if any("supply_air_pressure" in point for point in points):
            features["vav_count"] += 1  # VAV AHU
        else:
            features["cv_count"] += 1  # CV AHU

    for ahu, points in ahu_points.items():
        #print(f"AHU: {ahu}, Points: {points}")
        if any("supply_air_pressure" in point for point in points):
            print(f"  static pressure sensor found so classifing as a VAV AHU")
        else:
            print(f"  no static pressure sensor found so classifing as a CV AHU")
    return features


def identify_ahu_equipment(graph):
    """Combine results into a single AHU equipment dictionary."""
    ahu_equipment = {}
    ahu_equipment["ahu_count"] = count_ahus(graph)
    ahu_features = count_ahu_features(graph)
    ahu_equipment["ahu_features"] = ahu_features
    ahu_equipment["ahu_types"] = {
        "cv_count": ahu_features["cv_count"],
        "vav_count": ahu_features["vav_count"],
    }
    return ahu_equipment


def collect_ahu_data(ahu_info):
    """
    Collect AHU information and return it as structured data.
    """
    # Initialize dictionary for structured data
    ahu_data = {}

    # Total AHUs
    ahu_count = ahu_info.get("ahu_count", 0)
    ahu_data["Total AHUs"] = ahu_count

    # AHU Types
    ahu_types = ahu_info.get("ahu_types", {})
    ahu_data["Constant Volume AHUs"] = ahu_types.get("cv_count", 0)
    ahu_data["Variable Air Volume AHUs"] = ahu_types.get("vav_count", 0)

    # AHU Features
    ahu_features = ahu_info.get("ahu_features", {})
    ahu_data.update({
        "AHUs with Cooling Coil": ahu_features.get("cooling_coil_count", 0),
        "AHUs with Heating Coil": ahu_features.get("heating_coil_count", 0),
        "AHUs with DX Staged Cooling": ahu_features.get("dx_staged_cooling_count", 0),
        "AHUs with Return Fans": ahu_features.get("return_fan_count", 0),
        "AHUs with Supply Fans": ahu_features.get("supply_fan_count", 0),
        "AHUs with Return Air Temp Sensors": ahu_features.get("return_temp_count", 0),
        "AHUs with Mixing Air Temp Sensors": ahu_features.get("mixing_temp_count", 0),
        "AHUs with Leaving Air Temp Sensors": ahu_features.get("leaving_temp_count", 0),
        "AHUs with Leaving Air Temp Setpoint": ahu_features.get("leaving_air_temp_setpoint_count", 0),
        "AHUs with Duct Pressure Setpoint": ahu_features.get("duct_pressure_setpoint_count", 0),
        "AHUs with Duct Pressure": ahu_features.get("duct_pressure_count", 0),
    })

    return ahu_data
