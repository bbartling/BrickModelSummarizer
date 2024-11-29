import os
import pickle
from pydantic import BaseModel
from openai import OpenAI

# Path configurations
PICKLE_PATH = "acad.pkl"
BRICK_IN_TEXT_FILE_PATH = r"C:\Users\bbartling\Desktop\my-own-llm\ttl_to_text_tests\processed_data\acad.txt"

# Retrieve OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    exit(1)

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Define the structured response schema
class Step(BaseModel):
    explanation: str
    output: str

class BuildingReasoning(BaseModel):
    steps: list[Step]
    final_analysis: str

def load_text_until_keyword(file_path, keyword):
    """
    Load text from the file until the specified keyword is encountered.
    """
    content = []
    with open(file_path, "r") as file:
        for line in file:
            if keyword in line:
                print(f"Keyword '{keyword}' found. Stopping read.")
                break
            content.append(line.strip())
    return "\n".join(content)

def query_index(index, query, top_k=2):
    """
    Perform a query on the loaded FAISS index.
    """
    results = index.similarity_search(query, k=top_k)
    return results

def generate_building_reasoning(query, building_summary, embeddings_result):
    """
    Generate structured reasoning for building diagnostics with context.
    """
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are an expert in building HVAC systems and diagnostics. Provide a structured analysis for the user."},
                {"role": "user", "content": f"Building Summary:\n{building_summary}\n\nEmbeddings:\n{embeddings_result}\n\nQuery:\n{query}"}
            ],
            response_format=BuildingReasoning,
        )
        return completion.choices[0].message
    except Exception as e:
        print(f"Error during structured reasoning generation: {e}")
        exit(1)

if __name__ == "__main__":
    # Load the BRICK model summary
    print("Loading BRICK model summary...")
    BRICK_TEXT = load_text_until_keyword(BRICK_IN_TEXT_FILE_PATH, "Timeseries References")
    print("BRICK model summary loaded.")
    print("\nPreview of the loaded summary:")
    print(BRICK_TEXT[:500])

    # Load existing index
    print("Loading existing index...")
    if not os.path.exists(PICKLE_PATH):
        print(f"Pickle file {PICKLE_PATH} not found. Please create the index first.")
        exit(1)
    with open(PICKLE_PATH, "rb") as f:
        index = pickle.load(f)
    print(f"Index loaded from {PICKLE_PATH}")

    # Extract the first part of the BRICK summary for context
    building_summary = BRICK_TEXT.split("\n\n")[0]

    print("\nReady for queries!")
    while True:
        query = input("\nEnter your query (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break

        # Query the index for relevant embeddings
        results = query_index(index, query)
        embeddings_result = "\n".join([f"{i + 1}. {result.page_content}" for i, result in enumerate(results)])

        # Debug: Print the retrieved embeddings
        print("\nDEBUG: Retrieved embeddings used in LLM prompt:")
        print(embeddings_result)

        # Generate structured reasoning
        structured_reasoning = generate_building_reasoning(query, building_summary, embeddings_result)

        # Handle the response
        if structured_reasoning.refusal:
            print("Model refused to provide a response:")
            print(structured_reasoning.refusal)
        else:
            print("Structured Building Diagnostics Reasoning:")
            print(structured_reasoning.parsed.model_dump_json(indent=2))
