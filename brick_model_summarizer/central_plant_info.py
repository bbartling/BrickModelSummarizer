# central_plant_info.py
from brick_model_summarizer.utils import BRICK


def identify_hvac_system_equipment(graph):
    """Combine results from separate queries into a single dictionary for HVAC equipment."""
    hvac_equipment = {}
    hvac_equipment["hvac_system_counts"] = count_hvac_systems(graph)
    hvac_equipment["hvac_features"] = count_hvac_features(graph)
    return hvac_equipment


def count_hvac_systems(graph):
    """Count the total number of chillers, boilers, and cooling towers in the building model."""
    counts = {"chiller_count": 0, "boiler_count": 0, "cooling_tower_count": 0}
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    SELECT ?type (COUNT(?equip) AS ?count) WHERE {
        ?equip a ?type .
        FILTER(?type IN (brick:Chiller, brick:Boiler, brick:Cooling_Tower))
    } GROUP BY ?type
    """
    results = graph.query(query)
    for row in results:
        equip_type = str(row.type)
        count = int(row["count"])
        if equip_type == str(BRICK.Chiller):
            counts["chiller_count"] = count
        elif equip_type == str(BRICK.Boiler):
            counts["boiler_count"] = count
        elif equip_type == str(BRICK.Cooling_Tower):
            counts["cooling_tower_count"] = count
    return counts


def count_hvac_features(graph):
    """Count specific features for chillers, boilers, and cooling towers."""
    features = {
        "chiller_water_flow_count": 0,
        "boiler_water_flow_count": 0,
        "cooling_tower_fan_count": 0,
        "cooling_tower_temp_count": 0,
    }
    # Add queries for each feature if necessary
    # ...

    return features


def collect_central_plant_data(hvac_info):
    """
    Collect central plant equipment information as structured JSON-compatible data.
    """
    central_plant_data = {}

    # Collect central plant counts
    hvac_counts = hvac_info.get("hvac_system_counts", {})
    central_plant_data["total_chillers"] = hvac_counts.get("chiller_count", 0)
    central_plant_data["total_boilers"] = hvac_counts.get("boiler_count", 0)
    central_plant_data["total_cooling_towers"] = hvac_counts.get(
        "cooling_tower_count", 0
    )

    # Collect central plant features
    hvac_features = hvac_info.get("hvac_features", {})
    feature_details = {
        "chillers_with_water_flow": hvac_features.get("chiller_water_flow_count", 0),
        "boilers_with_water_flow": hvac_features.get("boiler_water_flow_count", 0),
        "cooling_towers_with_fan": hvac_features.get("cooling_tower_fan_count", 0),
        "cooling_towers_with_temp_sensors": hvac_features.get(
            "cooling_tower_temp_count", 0
        ),
    }

    central_plant_data.update(feature_details)

    return central_plant_data
