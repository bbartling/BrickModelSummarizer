import argparse
import glob
import os
from utils import load_graph, write_to_csv
from ahu_info import identify_ahu_equipment, print_ahu_info
from zone_info import identify_zone_equipment, print_zone_info
from meters_info import query_meters, print_meter_info
from central_plant_info import identify_hvac_system_equipment, print_central_plant_info
from building_info import print_building_info

# Define the path to the directory containing TTL files
directory_path = "./files/"


def process_file(file_path, save_csv):
    """Process a single TTL file and optionally save outputs to CSV."""
    filename = os.path.splitext(os.path.basename(file_path))[0]
    print(f"Processing: {filename}")

    graph = load_graph(file_path)

    # Define the CSV path if --save-csv is enabled
    csv_file_path = f"{directory_path}{filename}.csv" if save_csv else None

    # Delete the CSV file if it exists (to avoid appending to old data)
    if csv_file_path and os.path.exists(csv_file_path):
        print(f"Deleting old CSV file... {csv_file_path}")
        os.remove(csv_file_path)

    # Process each section and print/save to CSV
    ahu_info = identify_ahu_equipment(graph)
    print_ahu_info(ahu_info, csv_file_path)

    zone_info = identify_zone_equipment(graph)
    print_zone_info(zone_info, csv_file_path)

    print_building_info(graph, csv_file_path)

    meter_info = query_meters(graph)
    print_meter_info(meter_info, csv_file_path)

    hvac_info = identify_hvac_system_equipment(graph)
    print_central_plant_info(hvac_info, csv_file_path)


def main():
    parser = argparse.ArgumentParser(
        description="Run building analysis on all TTL files in the directory."
    )
    parser.add_argument(
        "--save-csv", action="store_true", help="Save metrics to CSV files when set"
    )
    args = parser.parse_args()

    # Loop over each TTL file in the specified directory
    for file_path in glob.glob(f"{directory_path}/*.ttl"):
        process_file(file_path, args.save_csv)


if __name__ == "__main__":
    main()
