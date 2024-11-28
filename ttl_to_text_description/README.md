# ttl to text description

This attempts to summarize BRICK model to a text file which could be used in the LLM RAG processes.

* TODO is to research if this is useful in giving the LLM context about the building.

## Arguments
- `--file <path>`: Path to a specific TTL file for processing. Use this to process a single file.
- `--save-csv`: Save metrics from TTL files to CSV files. Works with `--file` or all TTL files in the directory.
- `--analyze-csv`: Analyze CSV files for building type and ECMs.
- `--ttl-to-json`: Convert TTL files to JSON format for specific use cases.
- `--ttl-to-text`: Convert TTL files to a plain text description summarizing the building.
- `--output-dir <path>`: Directory to save output files. Defaults to `./processed_data`.

## Usage Examples

1. **Convert All TTL Files to Text Descriptions**:
   ```bash
   py .\main.py --ttl-to-text
   ```

2. **Convert a Specific TTL File to a Text Description**:
   ```bash
   py .\main.py --file ./files/bldg1.ttl --ttl-to-text
   ```

3. **Save All TTL Files as CSV**:
   ```bash
   py .\main.py --save-csv
   ```

4. **Analyze All CSV Files**:
   ```bash
   py .\main.py --analyze-csv
   ```

## Output Directory
All output files are saved in the directory specified by the `--output-dir` argument. By default, it is set to `./processed_data`.


