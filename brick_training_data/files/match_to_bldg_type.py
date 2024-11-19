import pandas as pd

# Building types with their descriptions, ECMs, and KPIs
building_types = {
    "Small and Medium Offices": {
        "description": "Small offices often rely on RTUs or split systems, while medium offices might use small chillers or multiple RTUs.",
        "ECMs": [
            "Load-based staging of RTUs",
            "Programmable thermostats for schedule alignment",
            "Use of economizers for free cooling"
        ],
        "KPIs": [
            "Run Time Reduction",
            "Energy per Occupied Area"
        ],
        "rules": {
            "area_max": 50000,  # sq ft
            "floors_max": 3,
            "chillers_max": 2,
            "central_plant": False
        }
    },
    "Large Offices": {
        "description": "Large offices have complex systems with multiple chillers, cooling towers, and pumps.",
        "ECMs": [
            "Chilled water and condenser temperature optimization",
            "VFDs on chillers and pumps",
            "Demand-based chiller staging"
        ],
        "KPIs": [
            "Energy Use Intensity",
            "Peak Demand Reduction",
            "Chiller Plant COP"
        ],
        "rules": {
            "area_min": 50000,  # sq ft
            "floors_min": 4,
            "chillers_min": 2,
            "central_plant": True
        }
    },
    # Add additional building types...
}

# Function to match CSV data to a building type
def match_building_type(csv_file, building_types):
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
        return "Error", {}

    # Map general column expectations to available columns in the file
    column_map = {
        "Building Area": ["Building Area", "Area", "Square Footage"],
        "Number of Floors": ["Number of Floors", "Floors", "Stories"],
        "Total Chillers": ["Total Chillers", "Chillers", "Cooling Units"],
        "Central Plant Features": ["Central Plant Features", "Plant Features", "Central Plant"]
    }

    # Dynamically map columns
    mapped_columns = {}
    for key, possible_columns in column_map.items():
        for col in possible_columns:
            if col in df.columns:
                mapped_columns[key] = col
                break

    if not mapped_columns:
        print(f"No recognizable columns in {csv_file}. Available columns: {list(df.columns)}")
        return "Unknown", {}

    # Extract relevant values, handling missing or unexpected data gracefully
    area = df[mapped_columns.get("Building Area")].iloc[0] if "Building Area" in mapped_columns else None
    floors = df[mapped_columns.get("Number of Floors")].iloc[0] if "Number of Floors" in mapped_columns else None
    chillers = df[mapped_columns.get("Total Chillers")].iloc[0] if "Total Chillers" in mapped_columns else None
    central_plant = (
        df[mapped_columns.get("Central Plant Features")].iloc[0] != "None"
        if "Central Plant Features" in mapped_columns
        else None
    )

    # Match to building type
    for building_type, details in building_types.items():
        rules = details["rules"]
        match = True

        # Check rule constraints
        if "area_min" in rules and area and area < rules["area_min"]:
            match = False
        if "area_max" in rules and area and area > rules["area_max"]:
            match = False
        if "floors_min" in rules and floors and floors < rules["floors_min"]:
            match = False
        if "floors_max" in rules and floors and floors > rules["floors_max"]:
            match = False
        if "chillers_min" in rules and chillers and chillers < rules["chillers_min"]:
            match = False
        if "chillers_max" in rules and chillers and chillers > rules["chillers_max"]:
            match = False
        if "central_plant" in rules and central_plant is not None and central_plant != rules["central_plant"]:
            match = False

        # If all conditions match, return the building type
        if match:
            return building_type, details

    # If no match found, return "Unknown"
    return "Unknown", {}

# Loop over all CSV files and attempt to match building type
csv_files = [
    "bldg1.csv", "bldg2.csv", "bldg3.csv",
    "bldg4.csv", "bldg5.csv", "bldg6.csv",
    "bldg7.csv", "bldg8.csv", "bldg9.csv",
    "bldg10.csv", "bldg11.csv", "bldg12.csv",
    "bldg13.csv", "bldg14.csv", "bldg15.csv"
]

for csv_file in csv_files:
    building_type, details = match_building_type(csv_file, building_types)
    print(f"File: {csv_file}")
    print(f"Matched Building Type: {building_type}")
    if details:
        print(f"Description: {details['description']}")
        print(f"ECMs: {', '.join(details['ECMs'])}")
        print(f"KPIs: {', '.join(details['KPIs'])}")
    else:
        print("No matching building type found.")
    print("-" * 40)
