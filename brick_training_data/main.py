import argparse
import glob
import os
from utils import load_graph, write_building_data_to_csv
from ahu_info import identify_ahu_equipment, collect_ahu_data
from zone_info import identify_zone_equipment, collect_zone_data
from meters_info import query_meters, collect_meter_data
from central_plant_info import identify_hvac_system_equipment, collect_central_plant_data
from building_info import collect_building_data

r"""
py .\main.py --file ./files/bldg1.ttl --save-csv
"""

# Define the path to the directory containing TTL files
directory_path = "./files/"

def print_kvs(data):
    # Loop through key-value pairs
    for key, value in data.items():
        print(f"{key}: {value}")


def process_file(file_path, save_csv):
    """Process a single TTL file and optionally save outputs to CSV."""
    filename = os.path.splitext(os.path.basename(file_path))[0]
    print(f"Processing: {filename}")

    graph = load_graph(file_path)

    building_data = {}

    # Define the CSV path if --save-csv is enabled
    csv_file_path = f"{directory_path}{filename}.csv" if save_csv else None

    # Delete the CSV file if it exists (to avoid appending to old data)
    if csv_file_path and os.path.exists(csv_file_path):
        print(f"Deleting old CSV file... {csv_file_path}")
        os.remove(csv_file_path)

    # Collect AHU Information
    ahu_info = identify_ahu_equipment(graph)
    building_data["AHU Information"] = collect_ahu_data(ahu_info)
    print_kvs(building_data["AHU Information"])
    print()

    # Collect Zone Information
    zone_info = identify_zone_equipment(graph)
    building_data["Zone Information"] = collect_zone_data(zone_info)
    print_kvs(building_data["Zone Information"])
    print()

    # Collect Building Information
    building_data["Building Information"] = collect_building_data(graph)
    print_kvs(building_data["Building Information"])
    print()

    # Collect Meter Information
    meter_info = query_meters(graph)
    building_data["Meter Information"] = collect_meter_data(meter_info)
    print_kvs(building_data["Meter Information"])
    print()

    # Collect Central Plant Information
    central_plant_info = identify_hvac_system_equipment(graph)
    building_data["Central Plant Information"] = collect_central_plant_data(central_plant_info)
    print_kvs(building_data["Central Plant Information"])
    print()

    # Save to CSV
    if save_csv:
        write_building_data_to_csv(building_data, csv_file_path)


def main():
    parser = argparse.ArgumentParser(
        description="Run building analysis on TTL files."
    )
    parser.add_argument(
        "--file", type=str, help="Path to a specific TTL file to process."
    )
    parser.add_argument(
        "--save-csv", action="store_true", help="Save metrics to CSV files when set."
    )
    args = parser.parse_args()

    if args.file:
        # Process the specified file
        if not os.path.exists(args.file):
            print(f"Error: File {args.file} does not exist.")
            return
        process_file(args.file, args.save_csv)
    else:
        # Process all TTL files in the directory
        for file_path in glob.glob(f"{directory_path}/*.ttl"):
            process_file(file_path, args.save_csv)


if __name__ == "__main__":
    main()
