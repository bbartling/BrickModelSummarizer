from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pickle
import os

# Text file and model paths
file_path = r"C:\Users\bbartling\Desktop\my-own-llm\ttl_to_text_tests\processed_data\acad.txt"
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
store_name = os.path.splitext(os.path.basename(file_path))[0]

# Read text data
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
chunks = text_splitter.split_text(text=content)

# Check for existing pickle file
if os.path.exists(f"my_data/{store_name}.pkl"):
    with open(f"my_data/{store_name}.pkl", "rb") as f:
        VectorStore = pickle.load(f)
else:
    # Use HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
    with open(f"{store_name}.pkl", "wb") as f:
        pickle.dump(VectorStore, f)

print("Done")
