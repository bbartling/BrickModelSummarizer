import requests
import os

# Define the base URL of your API
BASE_URL = "https://bensapi.pythonanywhere.com"

# Initialize a persistent session
session = requests.Session()

# Step 1: Visit the home page to get the session cookie
session.get(f"{BASE_URL}/")

# Step 2: Upload the TTL file
relative_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "sample_brick_models",
    "bldg6.ttl",
)
brick_model_file = os.path.abspath(os.path.normpath(relative_path))

if not os.path.exists(brick_model_file):
    raise FileNotFoundError(f"BRICK model file not found: {brick_model_file}")

# API endpoint URL for file upload
upload_url = f"{BASE_URL}/api/upload-ttl"

# Open the file and send the POST request with the session
try:
    with open(brick_model_file, "rb") as file:
        files = {"file": (brick_model_file, file)}
        response = session.post(upload_url, files=files)

        if response.status_code == 200:
            print("File uploaded successfully.")
        else:
            print(f"Upload failed: {response.status_code}")
            print(response.json())
            exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)

# Step 3: Retrieve all components dynamically
AVAILABLE_COMPONENTS = [
    "class_tag_summary",
    "ahu_information",
    "zone_information",
    "building_information",
    "meter_information",
    "central_plant_information",
    "number_of_vav_boxes_per_ahu",
]

component_url = f"{BASE_URL}/api/get-component"

# Dictionary to store all retrieved data
retrieved_data = {}

for component in AVAILABLE_COMPONENTS:
    params = {"component": component}
    response = session.get(component_url, params=params)

    if response.status_code == 200:
        retrieved_data[component] = response.json()
        print(f"{component} Data:\n", response.json(), "\n")
    else:
        print(f"Error fetching {component}: {response.status_code}")
        print(response.json())

# Step 4: Perform Basic Validation Like Pytest
expected_hvac_system_counts = {
    "total_variable_air_volume_boxes": 59,
    "water_pump": 4,
    "hot_water_system": 1,
    "hvac_equipment_count": 9,
}

# Extract relevant values from API responses
actual_hvac_system_counts = {
    "total_variable_air_volume_boxes": retrieved_data.get("zone_information", {}).get("total_variable_air_volume_boxes", 0),
    "water_pump": retrieved_data.get("central_plant_information", {}).get("water_pump", 0),
    "hot_water_system": retrieved_data.get("central_plant_information", {}).get("hot_water_system", 0),
    "hvac_equipment_count": retrieved_data.get("building_information", {}).get("hvac_equipment_count", 0),
}

print(f"Expected: {expected_hvac_system_counts}")
print(f"Actual: {actual_hvac_system_counts}")

print("=======================================")

assert actual_hvac_system_counts == expected_hvac_system_counts, (
    f"Mismatch in HVAC system counts. Expected: {expected_hvac_system_counts}, Actual: {actual_hvac_system_counts}"
)

print("All API responses match expected values!")
