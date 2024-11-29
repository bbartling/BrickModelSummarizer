import os
from pydantic import BaseModel
from openai import OpenAI

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

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

# Function to generate a step-by-step math reasoning response
def generate_math_reasoning(prompt):
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
                {"role": "user", "content": prompt}
            ],
            response_format=MathReasoning,
        )
        return completion.choices[0].message
    except Exception as e:
        print(f"Error during structured reasoning generation: {e}")
        exit(1)

# Main function
if __name__ == "__main__":

    prompt = "How can I solve 8x + 7 = -23?"
    
    # Generate the structured math reasoning
    math_reasoning = generate_math_reasoning(prompt)
    
    # Handle the response
    if math_reasoning.refusal:
        print("Model refused to provide a response:")
        print(math_reasoning.refusal)
    else:
        print("Structured Math Reasoning:")
        print(math_reasoning.parsed.model_dump_json(indent=2))

