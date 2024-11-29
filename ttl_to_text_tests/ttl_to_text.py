import os
from utils import load_graph
from csv_analyzer import analyze_csv, determine_building_type, suggest_ecms, suggest_kpis
from timeseries_references import extract_timeseries_references

def ttl_to_string(ttl_file):
    """Read the TTL file as a single string."""
    with open(ttl_file, 'r', encoding='utf-8') as file:
        return file.read()

def generate_text_description(summary, building_type, ecms, kpis, timeseries_references):
    """Generate a plain text description for the building."""
    lines = [
        f"Building Type: {building_type}",
        f"Total Floor Area: {summary.get('floor_area', 'Unknown')} sq ft",
        f"Number of Floors: {summary.get('num_floors', 'Unknown')}",
        f"Total AHUs: {summary.get('total_ahu_count', 0)}",
        f" - Variable Air Volume AHUs: {summary.get('vav_count', 0)}",
        f" - Constant Volume AHUs: {summary.get('cv_count', 0)}",
    ]

    equipment_counts = summary.get('equipment_counts', {})
    lines.append(f"Cooling Coils: {equipment_counts.get('Cooling Coils', 0)}")
    lines.append(f"Heating Coils: {equipment_counts.get('Heating Coils', 0)}")
    lines.append(f"Supply Fans: {equipment_counts.get('Supply Fans', 0)}")
    lines.append(f"Return Fans: {equipment_counts.get('Return Fans', 0)}")

    lines.append("\nRecommended Energy Conservation Measures (ECMs):")
    if ecms:
        for ecm in ecms:
            lines.append(f" - {ecm}")
    else:
        lines.append("None")

    lines.append("\nKey Performance Indicators (KPIs):")
    if kpis:
        for kpi in kpis:
            lines.append(f" - {kpi}")
    else:
        lines.append("None")

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

    # Load the TTL data and corresponding analysis
    graph = load_graph(ttl_file)
    ttl_string = ttl_to_string(ttl_file)
    csv_file_path = os.path.join("./files", f"{base_name}.csv")
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file {csv_file_path} does not exist. Ensure the CSV analysis step has been completed.")

    summary = analyze_csv(csv_file_path)
    building_type = determine_building_type(summary)
    ecms = suggest_ecms(summary)
    kpis = suggest_kpis(building_type)

    # Extract timeseries references
    timeseries_references = extract_timeseries_references(graph)

    # Generate text description
    description = generate_text_description(summary, building_type, ecms, kpis, timeseries_references)

    # Save the text description
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    text_file_path = os.path.join(output_dir, f"{base_name}.txt")

    with open(text_file_path, 'w', encoding='utf-8') as file:
        file.write(description)

    print(f"Generated text file: {text_file_path}")
