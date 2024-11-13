import json
from collections import defaultdict

# Load data from hvac-generic.json
with open('hvac-generic.json', 'r') as file:
    data = json.load(file)

# Create a dictionary to store entries based on their instruction, input, and output
entries = defaultdict(list)

# Check for duplicates
duplicates = []
for index, entry in enumerate(data):
    key = (entry['instruction'], entry['input'], entry['output'])
    if key in entries:
        duplicates.append((entries[key][0], index, entry))  # Store indices and entry of duplicates
    entries[key].append(index)

# Output the results
if duplicates:
    print("Duplicate entries found:")
    for first_index, second_index, entry in duplicates:
        print(f"Duplicate between entries at indices {first_index} and {second_index}")
        print(f"Instruction: {entry['instruction']}")
        print(f"Input: {entry['input']}")
        print(f"Output: {entry['output']}\n")
else:
    print("No duplicates found.")
