import argparse
import glob
import os
from utils import load_graph, write_building_data_to_csv
from ahu_info import identify_ahu_equipment, collect_ahu_data
from zone_info import identify_zone_equipment, collect_zone_data
from meters_info import query_meters, collect_meter_data
from central_plant_info import identify_hvac_system_equipment, collect_central_plant_data
from building_info import collect_building_data
from csv_analyzer import process_all_csvs

DEFAULT_DIRECTORY = "./files/"  # Default directory for TTL and CSV files

def ensure_directory_exists(directory):
    """Ensure the specified directory exists."""
    os.makedirs(directory, exist_ok=True)

def print_kvs(data):
    """Print key-value pairs."""
    for key, value in data.items():
        print(f"{key}: {value}")

def process_file(file_path, save_csv):
    """Process a single TTL file and optionally save outputs to CSV."""
    filename = os.path.splitext(os.path.basename(file_path))[0]
    print(f"Processing: {filename}")

    graph = load_graph(file_path)
    building_data = {}

    # Define the CSV path if --save-csv is enabled
    csv_file_path = os.path.join(DEFAULT_DIRECTORY, f"{filename}.csv") if save_csv else None

    # Delete the CSV file if it exists
    if csv_file_path and os.path.exists(csv_file_path):
        print(f"Deleting old CSV file... {csv_file_path}")
        os.remove(csv_file_path)

    # Collect AHU Information
    ahu_info = identify_ahu_equipment(graph)
    building_data["AHU Information"] = collect_ahu_data(ahu_info)
    print_kvs(building_data["AHU Information"])

    # Collect Zone Information
    zone_info = identify_zone_equipment(graph)
    building_data["Zone Information"] = collect_zone_data(zone_info)
    print_kvs(building_data["Zone Information"])

    # Collect Building Information
    building_data["Building Information"] = collect_building_data(graph)
    print_kvs(building_data["Building Information"])

    # Collect Meter Information
    meter_info = query_meters(graph)
    building_data["Meter Information"] = collect_meter_data(meter_info)
    print_kvs(building_data["Meter Information"])

    # Collect Central Plant Information
    central_plant_info = identify_hvac_system_equipment(graph)
    building_data["Central Plant Information"] = collect_central_plant_data(central_plant_info)
    print_kvs(building_data["Central Plant Information"])

    # Save to CSV
    if save_csv:
        write_building_data_to_csv(building_data, csv_file_path)

def main():
    parser = argparse.ArgumentParser(description="Run building analysis on TTL files.")
    parser.add_argument("--file", type=str, help="Path to a specific TTL file to process.")
    parser.add_argument("--save-csv", action="store_true", help="Save metrics to CSV files when set.")
    parser.add_argument("--analyze-csv", action="store_true", help="Analyze CSV files for building type and ECMs.")
    parser.add_argument("--ttl-to-json", action="store_true", help="Convert TTL to JSON for LLM fine-tuning.")
    parser.add_argument("--ttl-to-text", action="store_true", help="Convert TTL to plain text description.")
    parser.add_argument("--output-dir", type=str, default="./processed_data", help="Directory to save output files.")
    args = parser.parse_args()

    ensure_directory_exists(DEFAULT_DIRECTORY)
    ensure_directory_exists(args.output_dir)

    if args.file:
        base_filename = os.path.splitext(os.path.basename(args.file))[0]
        csv_file_path = os.path.join(DEFAULT_DIRECTORY, f"{base_filename}.csv")

        if args.analyze_csv:
            from csv_analyzer import analyze_csv, determine_building_type, suggest_ecms
            summary = analyze_csv(csv_file_path)
            if summary:
                building_type = determine_building_type(summary)
                ecms = suggest_ecms(summary)
                print(f"Detected Building Type: {building_type}")
                print("Suggested ECMs:")
                for ecm in ecms:
                    print(f" - {ecm}")

        elif args.ttl_to_text:
            from ttl_to_text import ttl_to_text
            ttl_to_text(args.file, args.output_dir)

        else:
            process_file(args.file, args.save_csv)
    elif args.ttl_to_text:
        from ttl_to_text import ttl_to_text
        print(f"Converting all TTL files in {DEFAULT_DIRECTORY} to text...")
        for ttl_file in glob.glob(f"{DEFAULT_DIRECTORY}/*.ttl"):
            ttl_to_text(ttl_file, args.output_dir)
    elif args.ttl_to_json:
        from ttl_to_json import ttl_to_json
        print(f"Converting all TTL files in {DEFAULT_DIRECTORY} to JSON...")
        for ttl_file in glob.glob(f"{DEFAULT_DIRECTORY}/*.ttl"):
            ttl_to_json(ttl_file, args.output_dir)
    else:
        print(f"Processing all TTL files in directory: {DEFAULT_DIRECTORY}")
        for file_path in glob.glob(f"{DEFAULT_DIRECTORY}/*.ttl"):
            process_file(file_path, args.save_csv)

if __name__ == "__main__":
    main()
