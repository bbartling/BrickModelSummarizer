import os
import json
from utils import load_graph
from csv_analyzer import analyze_csv, determine_building_type, suggest_ecms, suggest_kpis

def ttl_to_string(ttl_file):
    """Read the TTL file as a single string."""
    with open(ttl_file, 'r', encoding='utf-8') as file:
        ttl_data = file.read()
    return ttl_data

def generate_engineer_description(summary, building_type, ecms, kpis):
    """Generate a descriptive paragraph for the building."""
    description = (
        f"This building is categorized as a {building_type.lower()}, "
        f"with a total floor area of approximately {summary['floor_area']} square feet spanning {summary['num_floors']} floors. "
        f"The HVAC system comprises {summary['total_ahu_count']} air handling units (AHUs), "
        f"including {summary['vav_count']} variable air volume (VAV) units and {summary['cv_count']} constant volume (CV) units. "
    )
    if summary['equipment_counts']['Cooling Coils'] > 0:
        description += (
            f"The system includes {summary['equipment_counts']['Cooling Coils']} cooling coils, "
        )
    if summary['equipment_counts']['Heating Coils'] > 0:
        description += (
            f"{summary['equipment_counts']['Heating Coils']} heating coils, "
        )
    description += (
        f"and is equipped with advanced control features to optimize energy efficiency and occupant comfort. "
        f"To enhance performance, the following energy conservation measures (ECMs) are recommended: "
        f"{'; '.join(ecms)}. "
        f"In addition, the building's operational efficiency can be monitored using key performance indicators (KPIs) such as "
        f"{'; '.join(kpis)}."
    )
    return description

def ttl_to_json(ttl_file, output_dir):
    """
    Convert a Brick model TTL file into a JSON instruction format for fine-tuning.
    Includes the raw Brick model as 'input' and a descriptive paragraph as 'output'.
    """
    filename = os.path.basename(ttl_file)
    base_name = os.path.splitext(filename)[0]

    # Load the TTL data as a string
    ttl_string = ttl_to_string(ttl_file)

    # Analyze the corresponding CSV to generate a summary
    csv_file_path = os.path.join("./files", f"{base_name}.csv")
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file {csv_file_path} does not exist. Ensure the CSV analysis step has been completed.")

    summary = analyze_csv(csv_file_path)
    building_type = determine_building_type(summary)
    ecms = suggest_ecms(summary)
    kpis = suggest_kpis(building_type)

    # Generate the descriptive paragraph
    description = generate_engineer_description(summary, building_type, ecms, kpis)

    # Prepare the JSON structure
    json_data = {
        "instruction": f"Analyze the Brick model described in {ttl_file}",
        "input": ttl_string,  # Raw TTL content as input
        "output": description  # Engineer-style descriptive paragraph
    }

    # Save the JSON file to the output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    json_file_path = os.path.join(output_dir, f"{base_name}.json")

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4)

    print(f"Generated JSON file: {json_file_path}")
