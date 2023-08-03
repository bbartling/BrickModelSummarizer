
import os
import urllib.request



def download_file(file_link, filename):
    # Checks if the file already exists before downloading
    if not os.path.isfile(filename):
        urllib.request.urlretrieve(file_link, filename)
        print("File downloaded successfully.")
    else:
        print("File already exists.")
        

# comment out which model you want downloaded:
    
# Dowloading GGML model from HuggingFace
# ggml_model_path = "https://huggingface.co/CRD716/ggml-vicuna-1.1-quantized/resolve/main/ggml-vicuna-7b-1.1-q4_1.bin"
# filename = "ggml-vicuna-7b-1.1-q4_1.bin"

# ggml_model_path = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q6_K.bin"
# filename = "llama-2-7b-chat.ggmlv3.q6_K.bin"

ggml_model_path = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q2_K.bin"
filename = "llama-2-7b-chat.ggmlv3.q2_K.bin"

download_file(ggml_model_path, filename)

print("ALL DONE")