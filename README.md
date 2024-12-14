# BRICK Model to Text Description

This project transforms BRICK schema TTL files into concise, human-readable text summaries of building information. The goal is not only to provide clarity for humans but also to empower Large Language Models (LLMs) like ChatGPT to better understand and interpret complex building data.

From my initial testing, BRICK models—while highly structured—are often too intricate for LLMs to process effectively. These models present challenges due to their detailed and technical nature, making it difficult for LLMs to generate meaningful summaries or insights. This project addresses this issue by converting BRICK models into simplified summaries that retain essential information. The output aims to enable LLMs to reason about building systems with the perspective and analytical depth of a mechanical HVAC engineer, based on a clear summary of the mechanical systems embedded in the data. Can the LLM think like an engineer? I think so ...

## Writeups on Linkedin
* [Wait, What?! You Can Chat with Your Data Model?](https://www.linkedin.com/posts/ben-bartling-510a0961_buildingautomation-hvac-bas-activity-7268678804066197505-eWtn?utm_source=share&utm_medium=member_desktop)

## Features
- Summarizes BRICK schema TTL files into human-readable text files.
- Supports batch processing of multiple TTL files in a directory.
- Extracts key information about buildings, HVAC systems, meters, and zones.


## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/brick-model-to-text.git
   cd brick-model-to-text
   ```

2. **Install the required Python packages**:
   Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate

   ```
   Install dependencies:
   ```bash
   pip install rdflib pandas
   ```


## Arguments

| Argument          | Description                                                                                     |
|--------------------|-------------------------------------------------------------------------------------------------|
| `--file <path>`    | Path to a specific TTL file for processing. Use this to process a single file.                  |
| `--dir <path>`     | Directory containing TTL files for batch processing. Defaults to `./brick_model/`.              |
| `--ttl-to-text`    | Convert TTL files to plain text descriptions summarizing the building.                          |
| `--output-dir <path>` | Directory to save output text files. Defaults to `./processed_data`.                         |


## Usage Examples

### 1. **Process All TTL Files in the Default Directory**
Process all `.ttl` files in the `./brick_model/` directory and save the output to `./processed_data`:
```bash
python main.py --ttl-to-text --output-dir ./processed_data
```

### 2. **Process a Specific TTL File**
Process a specific `.ttl` file and generate a plain text summary:
```bash
python main.py --file ./brick_model/my_building.ttl --ttl-to-text --output-dir ./processed_data
```

### 3. **Process All TTL Files in a Custom Directory**
Specify a custom directory for input TTL files:
```bash
python main.py --dir ./custom_ttl_directory --ttl-to-text --output-dir ./custom_output
```

### 4. **Print Summaries Without Saving**
Print building summaries to the console for all TTL files in the directory (no text files saved):
```bash
python main.py
```

## Output Directory
All output files are saved in the directory specified by the `--output-dir` argument. By default, it is set to `./processed_data`. The output text files will have the same name as the corresponding TTL file, with a `.txt` extension.


## Dependencies
The project depends on the following Python packages:
- `rdflib`: For parsing and querying RDF graphs.
- Any additional packages listed in `requirements.txt`.

To install all dependencies, run:
```bash
pip install rdflib pandas
```

## Example Output
For a file named `bldg6.ttl`, the generated text file (`bldg6.txt`) which is a [reference BRICK model from BRICK schema.org](https://brickschema.org/resources/#reference-brick-models) the text file output will include:

```
AHU Information:
  - Total AHUs: 16
  - Constant Volume AHUs: 11
  - Variable Air Volume AHUs: 0
  - AHUs with Cooling Coil: 10
  - AHUs with Heating Coil: 7
  - AHUs with DX Staged Cooling: 0
  - AHUs with Return Fans: 0
  - AHUs with Supply Fans: 0
  - AHUs with Return Air Temp Sensors: 4
  - AHUs with Mixing Air Temp Sensors: 1
  - AHUs with Leaving Air Temp Sensors: 18
  - AHUs with Leaving Air Temp Setpoint: 9
  - AHUs with Duct Pressure Setpoint: 0
  - AHUs with Duct Pressure: 0
Zone Information:
  - Zone Air Temperature Setpoints: Zone Air Temperature Setpoints Found.
  - Total VAV Boxes: 132
  - Number of VAV Boxes per AHU: {'AHU: AH1S': 4, 'AHU: AH2N': 3, 'AHU: AH2S': 3, 'AHU: AH3S': 1, 'AHU: AHBS': 2, 'AHU: AHU01N': 24, 'AHU: AHU01S': 22, 'AHU: AHU02N': 10, 'AHU: AHU02S': 30, 'AHU: AHU03N': 14, 'AHU: AHU03S': 30}
  - VAV Boxes with Reheat Valve Command: 0
  - VAV Boxes with Air Flow Sensors: 0
  - VAV Boxes with Supply Air Temp Sensors: 0
  - VAV Boxes with Air Flow Setpoints: 0
  - Cooling Only VAV Boxes: 132
Building Information:
  - Building Area: 130149 sq ft
  - Number of Floors: 4
Meter Information:
  - BTU Meter Present: False
  - Electrical Meter Present: False
  - Water Meter Present: False
  - Gas Meter Present: False
  - PV Meter Present: False
Central Plant Information:
  - Total Chillers: 1
  - Total Boilers: 0
  - Total Cooling Towers: 0
  - Chillers with Water Flow: 0
  - Boilers with Water Flow: 0
  - Cooling Towers with Fan: 0
  - Cooling Towers with Temp Sensors: 0
```


If time series data base references are available in the model it will include data like this in the text file output:
```
Timeseries References:
 - Sensor: ACAD.AHU.AHU01.CCV
   Label: ACAD.AHU.AHU01.CCV
   Timeseries ID: 85bb0cab-3e62-33eb-963d-a418c4c8dcae
 - Sensor: ACAD.AHU.AHU01.Cooling_Valve_Output
   Label: ACAD.AHU.AHU01.Cooling Valve Output
   Timeseries ID: 79f48ae1-c476-3d3a-9938-61a90ceb2bd9
 - Sensor: ACAD.AHU.AHU01.Heating_Valve_Output
   Label: ACAD.AHU.AHU01.Heating Valve Output
   Timeseries ID: db852069-679f-360f-84df-c7119289709c
 - Sensor: ACAD.AHU.AHU01.Mixed_Air_Temp
   Label: ACAD.AHU.AHU01.Mixed Air Temp
   Timeseries ID: 11ad879d-23fd-38e2-9d06-01d671af5fa0
 - Sensor: ACAD.AHU.AHU01.Mode
   Label: ACAD.AHU.AHU01.Mode
   Timeseries ID: c784eada-7c2b-3a2d-85cd-9f504bd81153
```


## TODO
Work on generating a summary of suggested ECMs and KPIs based on the text file output.

## License
MIT