import os
from utils import load_graph
from ahu_info import identify_ahu_equipment, collect_ahu_data
from zone_info import identify_zone_equipment, collect_zone_data
from meters_info import query_meters, collect_meter_data
from central_plant_info import identify_hvac_system_equipment, collect_central_plant_data
from building_info import collect_building_data
from timeseries_references import extract_timeseries_references

def generate_text_description(building_data, timeseries_references):
    """Generate a plain text description for the building."""
    lines = []

    for category, details in building_data.items():
        lines.append(f"{category}:")
        if isinstance(details, dict):
            for subcategory, value in details.items():
                lines.append(f"  - {subcategory}: {value}")
        else:
            lines.append(f"  {details}")

    lines.append("\nTimeseries References:")
    if timeseries_references:
        for ref in timeseries_references:
            lines.append(f" - Sensor: {ref['sensor']}")
            lines.append(f"   Label: {ref['label']}")
            lines.append(f"   Timeseries ID: {ref['timeseries_id']}")
    else:
        lines.append("No Timeseries References Found.")

    return "\n".join(lines)


def ttl_to_text(ttl_file, output_dir):
    """Convert a Brick model TTL file into a plain text description."""
    filename = os.path.basename(ttl_file)
    base_name = os.path.splitext(filename)[0]

    # Load the TTL data
    graph = load_graph(ttl_file)

    # Collect data from the graph
    building_data = {}
    building_data["AHU Information"] = collect_ahu_data(identify_ahu_equipment(graph))
    building_data["Zone Information"] = collect_zone_data(identify_zone_equipment(graph))
    building_data["Building Information"] = collect_building_data(graph)
    building_data["Meter Information"] = collect_meter_data(query_meters(graph))
    building_data["Central Plant Information"] = collect_central_plant_data(identify_hvac_system_equipment(graph))

    # Extract timeseries references
    timeseries_references = extract_timeseries_references(graph)

    # Generate text description
    description = generate_text_description(building_data, timeseries_references)

    # Print the building summary to the console
    print("\n=== Building Summary ===")
    print(description)

    # Save the text description
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    text_file_path = os.path.join(output_dir, f"{base_name}.txt")

    with open(text_file_path, 'w', encoding='utf-8') as file:
        file.write(description)

    print(f"Generated text file: {text_file_path}")
