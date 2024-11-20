import os
import pandas as pd


def parse_building_area(area_str):
    """Convert a building area string like '10263 sq ft' to an integer."""
    if area_str and "sq ft" in area_str:
        try:
            return int(area_str.replace("sq ft", "").strip().replace(",", ""))
        except ValueError:
            return 0  # Default to 0 if parsing fails
    return 0  # Default to 0 for "Not available" or invalid values

def parse_number_of_floors(floor_str):
    """Convert a number of floors string to an integer."""
    if floor_str and floor_str.lower() != "not available":
        try:
            return int(floor_str.strip())
        except ValueError:
            return 0  # Default to 0 if parsing fails
    return 0  # Default to 0 for "Not available" or invalid values

def analyze_csv(file_path):
    """
    Analyze a single CSV file to extract relevant building information.
    """
    try:
        print(f"Debug: Reading CSV file {file_path}")
        df = pd.read_csv(file_path)
        print("Debug: CSV read successfully. Data preview:")
        print(df.head())  # Print the first few rows for debugging

        # Safely parse building area and number of floors
        try:
            building_area_row = df.loc[df["Subcategory"].str.contains("Building Area", na=False)]
            building_area_str = building_area_row["Details"].values[0] if not building_area_row.empty else "Not available"
        except Exception as e:
            print(f"Debug: Failed to parse Building Area - {e}")
            building_area_str = "Not available"

        try:
            num_floors_row = df.loc[df["Subcategory"].str.contains("Number of Floors", na=False)]
            num_floors_str = num_floors_row["Details"].values[0] if not num_floors_row.empty else "Not available"
        except Exception as e:
            print(f"Debug: Failed to parse Number of Floors - {e}")
            num_floors_str = "Not available"

        # Parse the extracted values
        floor_area = parse_building_area(building_area_str)
        num_floors = parse_number_of_floors(num_floors_str)

        print(f"Debug: Parsed floor area: {floor_area}, number of floors: {num_floors}")

        # Extract AHU and equipment data
        total_ahu_row = df.loc[df["Subcategory"].str.contains("Total AHUs", na=False)]
        total_ahu_count = int(total_ahu_row["Details"].values[0]) if not total_ahu_row.empty else 0

        vav_row = df.loc[df["Subcategory"].str.contains("Variable Air Volume AHUs", na=False)]
        vav_count = int(vav_row["Details"].values[0]) if not vav_row.empty else 0

        cv_row = df.loc[df["Subcategory"].str.contains("Constant Volume AHUs", na=False)]
        cv_count = int(cv_row["Details"].values[0]) if not cv_row.empty else 0

        # Equipment counts (e.g., Cooling Coils, Supply Fans)
        cooling_coils_row = df.loc[df["Subcategory"].str.contains("AHUs with Cooling Coil", na=False)]
        cooling_coils_count = int(cooling_coils_row["Details"].values[0]) if not cooling_coils_row.empty else 0

        # Construct summary
        summary = {
            "filename": os.path.basename(file_path),
            "floor_area": floor_area,
            "num_floors": num_floors,
            "total_ahu_count": total_ahu_count,
            "vav_count": vav_count,
            "cv_count": cv_count,
            "equipment_counts": {
                "Cooling Coils": cooling_coils_count,
                "Heating Coils": 0,  # Add logic for heating coils if necessary
                "Supply Fans": 0,  # Add logic for supply fans if necessary
                "Return Fans": 0,  # Add logic for return fans if necessary
            },
        }

        print(f"Debug: Extracted summary: {summary}")
        return summary

    except Exception as e:
        print(f"Error reading CSV {file_path}: {e}")
        return None


def determine_building_type(summary):
    """
    Determine the building type based on floor area and number of floors.
    """
    # Sample data for building type determination
    building_types = [
        {"name": "Large Office", "min_area": 498588, "max_area": float('inf'), "min_floors": 12, "max_floors": float('inf')},
        {"name": "Medium Office", "min_area": 53628, "max_area": 498587, "min_floors": 3, "max_floors": 11},
        {"name": "Small Office", "min_area": 0, "max_area": 53627, "min_floors": 1, "max_floors": 2},
        # Add other building types here
    ]

    # Retrieve building floor area and number of floors from summary
    try:
        floor_area = int(summary.get("floor_area", 0))  # Ensure this value is an integer
    except ValueError:
        floor_area = 0

    try:
        num_floors = int(summary.get("num_floors", 0))  # Ensure this value is an integer
    except ValueError:
        num_floors = 0

    # Determine the building type
    for building in building_types:
        if (building["min_area"] <= floor_area <= building["max_area"] and
                building["min_floors"] <= num_floors <= building["max_floors"]):
            return building["name"]

    return "Unknown Building Type"


def suggest_ecms(summary):
    """
    Suggest Energy Conservation Measures (ECMs) based on the summary.
    """
    ecms = []

    # Equipment-specific ECMs
    if summary["vav_count"] > 0:
        ecms.append("Implement Demand Control Ventilation (DCV) for VAV systems.")
    if summary["cv_count"] > 0:
        ecms.append("Convert CV systems to VAV systems for better efficiency.")
    if summary["equipment_counts"].get("Cooling Coils", 0) > 5:
        ecms.append("Optimize cooling coil operation during low-load periods.")
    if summary["equipment_counts"].get("Supply Fans", 0) > 5:
        ecms.append("Add variable frequency drives (VFDs) to supply fans.")

    # Building type-specific ECMs
    building_type = determine_building_type(summary)
    if building_type in ["Small Office", "Medium Office"]:
        ecms.extend([
            "Implement load-based staging of RTUs to minimize energy demand during low-occupancy periods.",
            "Adjust thermostat setpoints to align cooling schedules with office hours.",
            "Operate economizers to leverage outdoor air for free cooling when conditions permit.",
        ])
    if building_type == "Medium Office":
        ecms.extend([
            "Optimize HVAC scheduling to match occupancy levels.",
            "Upgrade BAS to improve zoning and control.",
        ])
    elif building_type == "Large Office":
        ecms.extend([
            "Optimize chilled water and condenser water temperatures to match cooling loads while maintaining efficiency.",
            "Equip chillers, pumps, and cooling towers with Variable Frequency Drives (VFDs) to modulate speed based on demand.",
            "Use demand-based staging to balance chiller loads, preventing unnecessary energy use and extending equipment life.",
        ])
    elif building_type == "Retail (Stand-alone or Strip Mall)":
        ecms.extend([
            "Schedule HVAC operation to coincide with business hours, reducing energy consumption during off-hours.",
            "Implement occupancy sensors to adjust temperature dynamically based on foot traffic and occupancy levels.",
        ])
    elif building_type in ["Primary School", "Secondary School"]:
        ecms.extend([
            "Adjust ventilation rates based on occupancy using Demand Control Ventilation (DCV).",
            "Implement seasonal cooling and heating setpoints to match school schedules, reducing unnecessary runtime.",
            "Utilize economizer modes to minimize mechanical cooling when outdoor conditions are favorable.",
        ])
    elif building_type in ["Hospital", "Outpatient Health Care"]:
        ecms.extend([
            "Optimize chilled water temperatures based on ambient conditions to improve chiller COP.",
            "Employ Variable-Speed Drives (VSDs) for pumps and fans to match HVAC operation with real-time demand.",
            "Use predictive maintenance and BAS data to avoid running equipment at unnecessarily high capacities.",
        ])
    elif building_type in ["Small Hotel", "Large Hotel"]:
        ecms.extend([
            "Adjust room temperature setpoints based on occupancy data to minimize energy use.",
            "Reclaim waste heat from chillers to produce domestic hot water efficiently.",
            "Participate in demand response programs by pre-conditioning spaces before peak hours.",
        ])
    elif building_type == "Warehouse (Non-Refrigerated)":
        ecms.extend([
            "Use occupancy sensors to control lighting and HVAC systems in warehouse zones.",
            "Maintain minimal HVAC levels to prevent excessive temperature fluctuations, preserving product quality.",
        ])
    elif building_type == "Quick Service & Full Service Restaurants":
        ecms.extend([
            "Use heat exchangers on exhaust systems to reclaim energy.",
            "Optimize ventilation rates based on kitchen activity to balance comfort and energy use.",
        ])
    elif building_type == "Apartments (Mid-Rise and High-Rise)":
        ecms.extend([
            "Monitor water use for cooling towers to improve efficiency.",
            "Adjust HVAC operation in common areas based on real-time occupancy data.",
        ])

    return ecms


def suggest_kpis(building_type):
    """
    Suggest Key Performance Indicators (KPIs) based on the building type.
    """
    kpis = []

    if building_type in ["Small Office", "Medium Office"]:
        kpis.extend([
            "Run Time Reduction: Measure total runtime of HVAC equipment.",
            "Energy per Occupied Area: Track energy consumption (kWh) relative to building occupancy.",
        ])
    elif building_type == "Large Office":
        kpis.extend([
            "Energy Use Intensity (EUI): Calculate kWh per square foot of building space.",
            "Peak Demand Reduction: Reduce peak power during occupied hours.",
            "Chiller Plant Coefficient of Performance (COP): Monitor chiller efficiency through load and water temperature adjustments.",
        ])
    elif building_type == "Retail (Stand-alone or Strip Mall)":
        kpis.extend([
            "Revenue per kWh: Assess energy efficiency in terms of sales generated per unit of energy consumed.",
            "Lighting and HVAC Energy Monitoring: Measure separately to optimize systems for different store types.",
        ])
    elif building_type in ["Primary School", "Secondary School"]:
        kpis.extend([
            "Ventilation Rate Compliance: Ensure required air changes per hour are met.",
            "Chiller Efficiency: Monitor energy consumption per ton of cooling to optimize high-demand operations.",
        ])
    elif building_type in ["Hospital", "Outpatient Health Care"]:
        kpis.extend([
            "Critical Systems Uptime: Ensure continuous HVAC operation to maintain patient care environments.",
            "Energy per Bed: Track energy usage efficiency in relation to hospital capacity.",
            "Thermal Storage Utilization: Measure peak shaving efficiency by storing chilled water during off-peak hours.",
        ])
    elif building_type in ["Small Hotel", "Large Hotel"]:
        kpis.extend([
            "Energy per Occupied Room: Align HVAC energy use with room occupancy.",
            "Guest Comfort Compliance: Maintain preferred temperature and humidity ranges in guest areas.",
            "COP and Load Tracking: Monitor and optimize chiller performance.",
        ])
    elif building_type == "Warehouse (Non-Refrigerated)":
        kpis.extend([
            "Lighting Utilization Efficiency: Reduce lighting energy through smart controls.",
            "Temperature Compliance: Ensure storage conditions meet product requirements.",
        ])
    elif building_type == "Quick Service & Full Service Restaurants":
        kpis.extend([
            "Utility Cost per Meal: Calculate HVAC and water costs per meal served.",
            "Ventilation Efficacy: Monitor energy use against peak occupancy levels.",
        ])
    elif building_type == "Apartments (Mid-Rise and High-Rise)":
        kpis.extend([
            "Energy per Occupied Unit: Measure energy use efficiency at the tenant level.",
            "Water Usage per Unit: Track water conservation metrics for cooling and domestic purposes.",
        ])

    return kpis


def process_all_csvs(directory):
    """
    Process all CSV files in the specified directory.
    """
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    all_summaries = []

    for csv_file in csv_files:
        print(f"Processing CSV: {csv_file}")
        summary = analyze_csv(csv_file)

        if summary:
            # Determine building type
            building_type = determine_building_type(summary)
            summary["matched_building_type"] = building_type
            print(f"Detected Building Type: {building_type}")

            # Suggest ECMs
            ecms = suggest_ecms(summary)
            summary["ecms"] = ecms
            print("Suggested ECMs:")
            for ecm in ecms:
                print(f" - {ecm}")

            all_summaries.append(summary)

    return all_summaries
