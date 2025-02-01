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
