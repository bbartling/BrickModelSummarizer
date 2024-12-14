import argparse
import glob
import os
from utils import load_graph
from ahu_info import identify_ahu_equipment, collect_ahu_data
from zone_info import identify_zone_equipment, collect_zone_data
from meters_info import query_meters, collect_meter_data
from central_plant_info import identify_hvac_system_equipment, collect_central_plant_data
from building_info import collect_building_data
from ttl_to_text import ttl_to_text

DEFAULT_DIRECTORY = "./brick_model/"

def ensure_directory_exists(directory):
    """Ensure the specified directory exists."""
    os.makedirs(directory, exist_ok=True)

def process_file(file_path):
    """Process a single TTL file and print building data."""
    print(f"Processing file: {file_path}")

    graph = load_graph(file_path)
    building_data = {}

    building_data["AHU Information"] = collect_ahu_data(identify_ahu_equipment(graph))
    building_data["Zone Information"] = collect_zone_data(identify_zone_equipment(graph))
    building_data["Building Information"] = collect_building_data(graph)
    building_data["Meter Information"] = collect_meter_data(query_meters(graph))
    building_data["Central Plant Information"] = collect_central_plant_data(identify_hvac_system_equipment(graph))

    for category, details in building_data.items():
        print(f"\n{category}:")
        if isinstance(details, dict):
            for subcategory, value in details.items():
                print(f"  - {subcategory}: {value}")
        else:
            print(f"  {details}")

def process_all_files(directory, output_dir, ttl_to_text_flag):
    """Process all TTL files in the directory."""
    ttl_files = glob.glob(os.path.join(directory, "*.ttl"))
    if not ttl_files:
        print(f"No TTL files found in {directory}")
        return

    for ttl_file in ttl_files:
        if ttl_to_text_flag:
            ttl_to_text(ttl_file, output_dir)
        else:
            process_file(ttl_file)

def main():
    parser = argparse.ArgumentParser(description="Run building analysis on TTL files.")
    parser.add_argument(
        "--file",
        type=str,
        help="Path to a specific TTL file to process. If not provided, all TTL files in the directory will be processed."
    )
    parser.add_argument("--ttl-to-text", action="store_true", help="Convert TTL to plain text description.")
    parser.add_argument("--output-dir", type=str, default="./processed_data", help="Directory to save output files.")
    parser.add_argument("--dir", type=str, default=DEFAULT_DIRECTORY, help="Directory containing TTL files.")
    args = parser.parse_args()

    ensure_directory_exists(args.output_dir)

    if args.file:
        if args.ttl_to_text:
            ttl_to_text(args.file, args.output_dir)
        else:
            process_file(args.file)
    else:
        print(f"Processing all TTL files in directory: {args.dir}")
        process_all_files(args.dir, args.output_dir, args.ttl_to_text)

if __name__ == "__main__":
    main()
