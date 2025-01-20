import os
from brick_model_summarizer.main import process_brick_file  # Import the processing function

def save_to_text_file(data, filename):
    """Save the building data to a text file."""
    lines = []

    for category, details in data.items():
        lines.append(f"{category}:")
        if isinstance(details, dict):
            for subcategory, value in details.items():
                lines.append(f"  - {subcategory}: {value}")
        else:
            lines.append(f"  {details}")
        lines.append("")  # Add a blank line between categories

    # Write the lines to the file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("\n".join(lines))

# Example BRICK model file
brick_model_file = r"C:\Users\ben\Documents\HvacGPT\sample_brick_models\bldg6.ttl"

# Call the function to process the file
building_data = process_brick_file(brick_model_file)

# Print the building data (optional)
print("\n=== Building Data Dictionary ===")
for key, value in building_data.items():
    print(f"{key}: {value}")

# Save the data to a text file in the current directory
output_filename = os.path.join(os.getcwd(), "building_summary.txt")
save_to_text_file(building_data, output_filename)

print(f"\nBuilding summary saved to: {output_filename}")
