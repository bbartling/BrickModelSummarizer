# BRICK Model Summarizer

**BRICK Model Summarizer** is a Python tool designed to validate and benchmark AI-generated BRICK models against reference models. It transforms complex BRICK schema TTL files into concise, human-readable summaries of HVAC systems, zones, meters, and central plants. By leveraging [reference BRICK models](https://brickschema.org/resources/#reference-brick-models), this tool enables users to validate AI-created models for consistency, accuracy, and adherence to expected standards.

## Purpose

The primary purpose of this repository is to provide a framework for summarizing BRICK models into HVAC-centric insights. This is especially useful for:
- **Benchmarking AI-generated BRICK models** against reference models.
- **Validating BRICK schemas** for completeness and alignment with building system expectations.
- **Empowering building engineers, analysts, and AI developers** with clear summaries of mechanical systems and operational data.

## Key Features

- **HVAC-Focused Summarization**: Extracts key details about AHUs, VAVs, meters, and central plant equipment.
- **Model Validation**: Provides a framework for benchmarking AI-created BRICK models.
- **Scalable Processing**: Processes individual or multiple BRICK schema TTL files.
- **Ready-to-Use Outputs**: Generates text summaries suitable for validation, reporting, or further analysis.

## Installation
```bash
pip install brick-model-summarizer
```

### Local Installation for development purposes

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/brick-model-summarizer.git
   cd brick-model-summarizer
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   ```

3. **Install the package locally**:
   ```bash
   pip install .
   ```

## Usage

The package includes functions for summarizing BRICK models and generating detailed outputs. Below is a simple example of how to use the tool in Python:

### Example: Processing a BRICK Model
```python
from brick_model_summarizer.main import process_brick_file

# Path to the BRICK schema TTL file
brick_model_file = "sample_brick_models/bldg6.ttl"

# Generate a summary
building_data = process_brick_file(brick_model_file)

# Optionally, save the output as a text file
output_file = "bldg6_summary.txt"
with open(output_file, 'w') as file:
    for key, value in building_data.items():
        file.write(f"{key}:\n")
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                file.write(f"  - {sub_key}: {sub_value}\n")
        else:
            file.write(f"  {value}\n")
```

### Example Output
```
AHU Information:
  - Total AHUs: 16
  - Constant Volume AHUs: 11
  - Variable Air Volume AHUs: 0
  - AHUs with Cooling Coil: 10
  - AHUs with Heating Coil: 7
  ...

Zone Information:
  - Total VAV Boxes: 132
  - Cooling Only VAV Boxes: 132
  ...
```

### Validating AI-Generated Models
Use the outputs to compare AI-created models against reference BRICK models, checking for consistency in:
- Equipment classification (e.g., AHUs, VAVs).
- Sensor and control points.
- Central plant configurations.

## Sample Data

Reference BRICK models from [BRICK resources](https://brickschema.org/resources/#reference-brick-models) are included in the `sample_brick_models` directory. These files can be used for testing and validation.

## Contributing

We welcome contributions to improve the repository. Please submit issues or pull requests to discuss new features, bug fixes, or enhancements.

## Roadmap

### Planned Enhancements
- **ECM and KPI Suggestions**: Develop functionality to recommend energy conservation measures (ECMs) based on model summaries.
- **Advanced Validation**: Add checks for missing or inconsistent relationships in AI-generated models.
- **PyPI Distribution**: Prepare the package for publication on PyPI.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
