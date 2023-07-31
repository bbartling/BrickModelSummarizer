
import os
import urllib.request

def download_file(file_link, filename):
    # Checks if the file already exists before downloading
    if not os.path.isfile(filename):
        urllib.request.urlretrieve(file_link, filename)
        print("File downloaded successfully.")
    else:
        print("File already exists.")
        
        
# Dowloading GGML model from HuggingFace
ggml_model_path = "https://huggingface.co/CRD716/ggml-vicuna-1.1-quantized/resolve/main/ggml-vicuna-7b-1.1-q4_1.bin"
filename = "ggml-vicuna-7b-1.1-q4_1.bin"

download_file(ggml_model_path, filename)