
This Python script demonstrates how to send a `.ttl` file to the BRICK Model Summarizer API using a POST request and receive a detailed JSON response.

## Requirements

Ensure you have Python installed, along with the `requests` library. Install the library if needed:

```bash
pip install requests
```

## Usage

1. **Start the Flask API Server**

   Make sure the BRICK Model Summarizer Flask app is running. To use Bens Flask App on backend API request try:

   ```
   url = "https://bensapi.pythonanywhere.com/api/process-ttl"
   ```

   Adjust the URL if your server is hosted on a different host or port. 

2. **Run the Client Script**

   Save the following Python code as `client_post.py` or another filename:

   ```python
   import requests

   # API endpoint URL
   url = "http://127.0.0.1:5000/api/process-ttl"

   # Path to the .ttl file
   file_path = "/path/to/your/file.ttl"

   try:
       print("brick_model_file: ", file_path)

       # Open the file and send the POST request
       with open(file_path, 'rb') as file:
           files = {'file': (file_path, file)}
           response = requests.post(url, files=files)

           if response.status_code == 200:
               # Display the processed data
               print("Processed Data:")
               print(response.json())
           else:
               print(f"Error {response.status_code}: {response.json()}")

   except FileNotFoundError:
       print("The specified file was not found.")
   except Exception as e:
       print(f"An error occurred: {e}")
   ```

3. **Execute the Script**

   Run the script from your terminal or command line:

   ```bash
   python client_post.py
   ```

4. **Expected Output**

   Upon a successful POST request, the script will print the processed JSON data:

   ```plaintext
   brick_model_file:  /home/ben/bldg6.ttl
   Processed Data:
   {
       "AHU Information": {
           "AHUs with Cooling Coil": 10,
           "Constant Volume AHUs": 11,
           ...
       },
       "Building Information": {
           "Building Area": "130149 sq ft",
           "Number of Floors": 4
       },
       ...
   }
   ```

## Notes

- Replace `/path/to/your/file.ttl` with the actual path to your `.ttl` file.
- The API will reject non-`.ttl` files, ensuring compatibility with the BRICK model.

## Troubleshooting

- If you encounter issues, ensure the Flask app is running and accessible at the specified URL.
- Verify the `.ttl` file path is correct and the file exists.
