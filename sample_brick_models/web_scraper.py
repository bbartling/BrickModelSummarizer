import requests
import os

# Directory to save the downloaded .ttl files
data_dir = 'brick_training_data'
os.makedirs(data_dir, exist_ok=True)

# Base URL for the .ttl files
base_url = "https://brickschema.org/ttl/mortar/"

# Download the numbered .ttl files (bldg1.ttl to bldg41.ttl)
for i in range(1, 42):
    url = f"{base_url}bldg{i}.ttl"
    file_name = os.path.join(data_dir, f"bldg{i}.ttl")
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        
        # Save the .ttl file content
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)
        
        print(f"Downloaded: {url} -> {file_name}")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to download {url}: {e}")

# Download the smc.ttl file separately
smc_url = f"{base_url}smc.ttl"
smc_file_name = os.path.join(data_dir, "smc.ttl")

try:
    response = requests.get(smc_url)
    response.raise_for_status()
    
    # Save the .ttl file content
    with open(smc_file_name, 'w', encoding='utf-8') as file:
        file.write(response.text)
    
    print(f"Downloaded: {smc_url} -> {smc_file_name}")
except requests.exceptions.HTTPError as e:
    print(f"Failed to download {smc_url}: {e}")
