from langchain.embeddings import LlamaCppEmbeddings
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import LlamaCppEmbeddings
from langchain.vectorstores import FAISS
import os

# https://python.langchain.com/docs/integrations/vectorstores/faiss

file_path = "my_data/hvac.txt"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, length_function=len
)
chunks = text_splitter.split_text(text=content)

store_name = os.path.splitext(os.path.basename(file_path))[0]
print(f"Using store name: {store_name}")

if os.path.exists(f"{store_name}.pkl"):
    with open(f"my_data/{store_name}.pkl", "rb") as f:
        VectorStore = pickle.load(f)
else:
    embeddings = LlamaCppEmbeddings(model_path="./model/ggml-vicuna-7b-1.1-q4_1.bin")
    VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
    with open(f"my_data/{store_name}.pkl", "wb") as f:
        pickle.dump(VectorStore, f)
        
print("Done")