import pandas as pd
from rdflib import Graph, Namespace

# Helper function to sanitize URIs (must match the one in make_brick_model.py)
def sanitize_uri(label):
    """Sanitize the label to create a valid URI."""
    return label.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_").replace("%", "")

# Load the BRICK model
def load_brick_model(file_path):
    g = Graph()
    g.parse(file_path, format="turtle")
    return g

# Extract CSV column mappings from the BRICK model
def extract_csv_columns(graph):
    BRICK = Namespace("https://brickschema.org/schema/Brick#")
    EX = Namespace("http://example.com/building#")

    # Query the BRICK model to map URIs to sanitized CSV column names
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX ex: <http://example.com/building#>
    SELECT ?point ?label WHERE {
        ?point a ?type ;
               brick:isPointOf ex:AHU1 .
        BIND(STRAFTER(STR(?point), "building#") AS ?label)
    }
    """
    results = graph.query(query)

    # Return a mapping of BRICK concepts to sanitized column names
    return {str(row[0]): sanitize_uri(str(row[1])) for row in results}

def perform_fault_detection(csv_file, column_mapping):
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Print CSV columns
    print("\n[INFO] Columns in the CSV file:")
    print(df.columns.tolist())

    # Dynamically match sanitized BRICK labels to actual CSV column names
    csv_columns = {}
    for uri, sanitized_label in column_mapping.items():
        matched_column = next(
            (col for col in df.columns if sanitize_uri(col) == sanitized_label), None
        )
        if matched_column:
            csv_columns[uri] = matched_column
        else:
            print(f"[WARNING] Could not find a matching column in the CSV for BRICK reference: {uri} ({sanitized_label})")

    # Print the mapping of BRICK URIs to CSV columns
    print("\n[INFO] Mapped BRICK references to CSV columns:")
    for uri, col in csv_columns.items():
        print(f"  BRICK: {uri} -> CSV: {col}")

    # Check for missing columns
    missing_columns = [
        sanitized_label for uri, sanitized_label in column_mapping.items() if uri not in csv_columns
    ]
    if missing_columns:
        raise ValueError(f"[ERROR] Missing required columns in CSV: {', '.join(missing_columns)}")

    # Fault detection thresholds
    static_threshold = 0.1  # Threshold for static pressure
    fan_speed_min = 95  # Minimum fan speed in percentage
    rolling_window = 3  # Rolling window size for fault detection

    # Correctly use the mapped BRICK URIs
    try:
        df["fc1_flag"] = (
            (df[csv_columns["http://example.com/building#AHU1_SaStatic_value_in_wc"]]
             < (df[csv_columns["http://example.com/building#AHU1_Eff_StaticSPt"]] - static_threshold)) &
            (df[csv_columns["http://example.com/building#AHU1_SaFanSpeedAO_value_"]] >= fan_speed_min)
        ).rolling(window=rolling_window).sum() == rolling_window
    except KeyError as e:
        print(f"[ERROR] KeyError: {e}. Please check the column mappings and BRICK model.")
        raise

    # Save processed results
    output_csv = "processed_hvac_data.csv"
    df.to_csv(output_csv, index=False)
    print(f"\n[INFO] Fault detection complete. Processed data saved to {output_csv}.")
    
    # Check counts of fc1_flag values
    print("\n[INFO] Counts of fc1_flag values:")
    print(df["fc1_flag"].value_counts())


# Main execution
if __name__ == "__main__":
    # Load the BRICK model
    brick_file = "brick_model.ttl"
    graph = load_brick_model(brick_file)

    # Extract CSV column mappings
    column_mapping = extract_csv_columns(graph)

    # Print the extracted BRICK references
    print("\n[INFO] Extracted BRICK references:")
    for uri, sanitized_label in column_mapping.items():
        print(f"  BRICK: {uri} -> Sanitized: {sanitized_label}")

    # Perform fault detection
    csv_file = "hvac_data.csv"
    perform_fault_detection(csv_file, column_mapping)
