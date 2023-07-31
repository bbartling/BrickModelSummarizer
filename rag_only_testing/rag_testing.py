
from transformers import RagTokenForGeneration, RagTokenizer, RagRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
import torch


def split_text_into_chunks(text, chunk_size, overlap):
    """
    Split the text into chunks of the specified size with an overlap.
    
    Parameters:
    - text (str): The input text to be split.
    - chunk_size (int): The size of each chunk.
    - overlap (int): The size of the overlap between chunks.
    
    Returns:
    - list of str: The split text chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# Load the text file from the data subdirectory
with open('my_data/hvac.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Split the content using the text splitter utility
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
sections = split_text_into_chunks(content, 1000, 200)

# Load the RAG model and its components
model_name = 'facebook/rag-sequence-nq'
model = RagTokenForGeneration.from_pretrained(model_name)
tokenizer = RagTokenizer.from_pretrained(model_name)
retriever = RagRetriever.from_pretrained(model_name, index_name="exact", use_dummy_dataset=True)

model.set_retriever(retriever)

while True:
    prompt = input("\nEnter a prompt (or type 'exit' to quit): ")
    if prompt.lower() == "exit":
        break
    else:
        # Use the query as an input document
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids

        # Find the most relevant passage
        passages = [f"Passage {i}: {section}" for i, section in enumerate(sections)]
        retrieval_input_ids = tokenizer(passages, return_tensors="pt", padding=True, truncation=True).input_ids
        with torch.no_grad():
            # You can control how many passages to retrieve with 'num_return_sequences'
            retriever_results = retriever.retrieve(input_ids=input_ids, documents=retrieval_input_ids)

        # Generate text using the retrieved passages as context
        with torch.no_grad():
            generated = model.generate(input_ids=retriever_results["input_ids"], attention_mask=retriever_results["attention_mask"], max_length=100)
        generated_text = tokenizer.decode(generated[0], skip_special_tokens=True)

        print("\nGenerated text from RAG:\n")
        print(generated_text)