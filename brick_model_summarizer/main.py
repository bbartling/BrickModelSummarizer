from brick_model_summarizer.utils import load_graph
from brick_model_summarizer.ahu_info import identify_ahu_equipment, collect_ahu_data
from brick_model_summarizer.zone_info import identify_zone_equipment, collect_zone_data
from brick_model_summarizer.meters_info import query_meters, collect_meter_data
from brick_model_summarizer.central_plant_info import (
    identify_hvac_system_equipment,
    collect_central_plant_data,
)
from brick_model_summarizer.building_info import collect_building_data
from brick_model_summarizer.class_tag_checker import analyze_classes_and_tags


def load_graph_once(brick_model_file):
    """Load the RDF graph once to prevent redundant loading."""
    return load_graph(brick_model_file)


def get_class_tag_summary(graph):
    """Return class tag summary."""
    return analyze_classes_and_tags(graph)


def get_ahu_information(graph):
    """Return AHU information."""
    return collect_ahu_data(identify_ahu_equipment(graph))


def get_zone_information(graph):
    """Return zone information."""
    zone_info = identify_zone_equipment(graph)
    return collect_zone_data(zone_info)


def get_building_information(graph):
    """Return building information."""
    return collect_building_data(graph)


def get_meter_information(graph):
    """Return meter information."""
    return collect_meter_data(query_meters(graph))


def get_central_plant_information(graph):
    """Return central plant information."""
    return collect_central_plant_data(identify_hvac_system_equipment(graph))


def get_vav_boxes_per_ahu(graph):
    """Return VAV boxes per AHU information."""
    zone_info = identify_zone_equipment(graph)
    return zone_info.get("vav_per_ahu", {})
