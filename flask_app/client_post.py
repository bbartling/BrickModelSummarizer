import requests
import os


relative_path = os.path.join(
    os.path.dirname(__file__),  # Directory of the current script
    "..",  # Go up one level to the project root
    "sample_brick_models",  # Subdirectory for Brick models
    "bldg6.ttl",  # The Brick model file
)
brick_model_file = os.path.abspath(os.path.normpath(relative_path))
print("brick_model_file: ",brick_model_file)

# API endpoint URL
url = "https://bensapi.pythonanywhere.com/api/process-ttl"

# Open the file in binary mode and send the POST request
try:
    with open(brick_model_file, 'rb') as file:
        # Prepare the files payload
        files = {'file': (brick_model_file, file)}
        
        # Send the POST request
        response = requests.post(url, files=files)
        
        # Check if the response is successful
        if response.status_code == 200:
            # Parse and display the JSON response
            data = response.json()
            print("Processed Data:")
            print(data)
        else:
            print(f"Error: {response.status_code}")
            print(response.json())
except FileNotFoundError:
    print("The specified file was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
