import pandas as pd
from rdflib import Graph, Namespace
from rdflib.namespace import RDF

# Namespaces
BRICK = Namespace("https://brickschema.org/schema/Brick#")
REF = Namespace("https://brickschema.org/schema/Brick/ref#")

# Load BRICK model
def load_brick_model(brick_file):
    g = Graph()
    g.parse(brick_file, format="turtle")
    return g

# Extract points of interest from BRICK model
def extract_points(graph):
    """
    Extract timeseries points for fan speed and static pressure.
    """
    fan_speed_point = None
    static_pressure_point = None
    setpoint_point = None

    for point, _, obj in graph.triples((None, RDF.type, None)):
        print(f"Checking Point: {point}, Type: {obj}")  # Debug print
        if obj == BRICK.Supply_Fan_Speed_Command:
            fan_speed_point = graph.value(point, REF.hasTimeseriesId)
            print(f"Fan Speed Point found: {fan_speed_point}")  # Debug print
        elif obj == BRICK.Supply_Air_Static_Pressure_Sensor:
            static_pressure_point = graph.value(point, REF.hasTimeseriesId)
            print(f"Static Pressure Point found: {static_pressure_point}")  # Debug print
        elif obj == BRICK.Supply_Air_Static_Pressure_Setpoint:
            setpoint_point = graph.value(point, REF.hasTimeseriesId)
            print(f"Setpoint Point found: {setpoint_point}")  # Debug print

    return str(fan_speed_point) if fan_speed_point else None, \
           str(static_pressure_point) if static_pressure_point else None, \
           str(setpoint_point) if setpoint_point else None

# Fault detection logic
def detect_faults(df, fan_speed_col, static_pressure_col, setpoint_col):
    """
    Detect faults where fan speed > 95% and duct static pressure < setpoint.
    """
    faults = df[(df[fan_speed_col] > 95) & (df[static_pressure_col] < df[setpoint_col])]
    return faults

# Main function
def main():
    # File paths
    brick_file = "brick_model_with_refs.ttl"
    csv_file = "building_data.csv"

    # Load BRICK model
    print("Loading BRICK model...")
    brick_graph = load_brick_model(brick_file)

    # Extract points of interest
    print("Extracting points of interest...")
    fan_speed_col, static_pressure_col, setpoint_col = extract_points(brick_graph)
    print(f"Fan Speed Column: {fan_speed_col}")
    print(f"Static Pressure Column: {static_pressure_col}")
    print(f"Setpoint Column: {setpoint_col}")

    # Load CSV data
    print("Loading CSV data...")
    df = pd.read_csv(csv_file)

    for col in df.columns:
        print(col)

    # Perform fault detection
    print("Detecting faults...")
    faults = detect_faults(df, fan_speed_col, static_pressure_col, setpoint_col)

    # Display faults
    if not faults.empty:
        print("Faults detected:")
        print(faults)
    else:
        print("No faults detected.")

if __name__ == "__main__":
    main()
