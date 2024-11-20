# Building Analysis Script

This script processes TTL files describing building information into CSV or JSON formats and analyzes the building's key metrics for ECMs and building type.

## Arguments
- `--file <path>`: Path to a specific TTL file for processing. Use this to process a single file.
- `--save-csv`: Process TTL files and save their metrics to corresponding CSV files. Works with `--file` or on all TTL files in the directory.
- `--analyze-csv`: Analyze all CSV files or a specific CSV file to detect building type and suggest ECMs.
- `--ttl-to-json`: Convert all TTL files (or a specific TTL file with `--file`) into JSON format suitable for fine-tuning machine learning models.
- `--output-dir <path>`: Directory to save JSON files when using `--ttl-to-json`. Defaults to `./processed_fine_tune_data`.

## Usage Examples
1. **Process a Single File and Save to CSV**:
   ```bash
   py .\main.py --file ./files/bldg1.ttl --save-csv
   ```

### Steps to Loop Over All Files
1. **Convert All TTL Files to JSON**  
   Use the `--ttl-to-json` argument to convert all TTL files in the default directory to JSON files in the output directory:
   ```bash
   py .\main.py --ttl-to-json
   ```

2. **Save All TTL Files as CSV**  
   Use the `--save-csv` argument to process all TTL files in the default directory and save them as CSV:
   ```bash
   py .\main.py --save-csv
   ```

3. **Analyze All CSV Files**  
   Use the `--analyze-csv` argument to analyze all CSV files in the default directory:
   ```bash
   py .\main.py --analyze-csv
   ```

4. **Process a Specific File**  
   Add the `--file` argument to process a single file with additional options like saving to CSV or analyzing it:
   ```bash
   py .\main.py --file ./files/bldg1.ttl --save-csv
   ```

2. **Analyze a Specific CSV File**:
   ```bash
   py .\main.py --file ./files/bldg1.ttl --analyze-csv
   ```

3. **Convert All TTL Files to JSON**:
   ```bash
   py .\main.py --ttl-to-json
   ```

4. **Process All TTL Files and Save to CSV**:
   ```bash
   py .\main.py --save-csv
   ```

5. **Analyze All CSV Files**:
   ```bash
   py .\main.py --analyze-csv
   ```

## Default Directory
The default directory for TTL and CSV files is `./files/`. Ensure your files are stored here before running batch commands.

## Output Directory
JSON files generated during the `--ttl-to-json` process will be saved in the directory specified by `--output-dir`. Defaults to `./processed_fine_tune_data/`.
