import json

# Read the TTL file as a single string
def ttl_to_string(ttl_file):
    with open(ttl_file, 'r', encoding='utf-8') as file:
        ttl_data = file.read()
    return ttl_data

# Convert the TTL string into a JSON structure
def ttl_to_json_string(ttl_file, output_json_file):
    ttl_string = ttl_to_string(ttl_file)
    json_data = {
        "instruction": f"Analyze the Brick model described in {ttl_file}",
        "input": ttl_string,
        "output": "Provide a summary of the HVAC system, zones, and central plant features based on the Brick model."
    }
    
    # Save as JSON
    with open(output_json_file, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4)
    
    print(f"Converted {ttl_file} into JSON format at {output_json_file}")

# Convert bldg1.ttl to a JSON file
ttl_to_json_string('bldg1.ttl', 'bldg1_instruction.json')
