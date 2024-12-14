# BRICK Model to Text Description

This project transforms BRICK schema TTL files into concise, human-readable text summaries of building information. The goal is not just to provide clarity for humans but also to enable Large Language Models (LLMs) like ChatGPT to better understand and interpret building data.

Currently, BRICK models are highly structured but often too complex for LLMs to comprehend directly, as evidenced by initial tests where LLMs struggled to summarize these models effectively. This project bridges the gap by converting BRICK models into a format that simplifies their complexity, enabling LLMs to approach building systems with the reasoning and insight of an engineer.

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
For a file named `my_building.ttl`, the generated text file (`my_building.txt`) will include:
```
AHU Information:
  - Total AHUs: 3
  - Constant Volume AHUs: 2
  - Variable Air Volume AHUs: 1
...

Zone Information:
  - Total VAV Boxes: 12
  - VAV Boxes with Air Flow Sensors: 10
...

Building Information:
  - Building Area: 10263 sq ft
  - Number of Floors: 3
...

Timeseries References:
  - Sensor: Zone_Temp_Sensor
    Label: Zone Temperature
    Timeseries ID: ts_001
...
```

