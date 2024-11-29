import os
import io
import sys
from pydantic import BaseModel
from openai import OpenAI

# Retrieve OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    exit(1)

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Define structured response schema
class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

# Function to generate a structured math reasoning response
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

# Function to save math reasoning to a Python file
def save_to_file(reasoning, filename="math_reasoning.py"):
    try:
        with open(filename, "w") as file:
            file.write("# Auto-generated Python script for math reasoning\n")
            file.write("def solve_equation():\n")
            for step in reasoning.steps:
                explanation = step.explanation.replace('"', '\\"')
                output = step.output.replace('"', '\\"')
                file.write(f"    # {explanation}\n")
                file.write(f"    print('{output}')\n")
            file.write(f"\n    print('Final Answer: {reasoning.final_answer}')\n")
            file.write("\nif __name__ == '__main__':\n")
            file.write("    solve_equation()\n")
        print(f"Generated reasoning saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")

# Function to execute the saved Python file
def execute_file(filename):
    try:
        captured_output = io.StringIO()
        sys.stdout = captured_output  # Redirect stdout
        os.system(f"python {filename}")
        sys.stdout = sys.__stdout__  # Reset stdout
        return captured_output.getvalue()
    except Exception as e:
        print(f"Error executing the file: {e}")
        sys.stdout = sys.__stdout__  # Reset stdout in case of error

# Main function
if __name__ == "__main__":
    # Prompt for solving a math problem
    prompt = "How can I solve 8x + 7 = -23?"
    
    # Generate the structured math reasoning
    math_reasoning = generate_math_reasoning(prompt)
    
    # Check if the model refused the request
    if math_reasoning.refusal:
        print("Model refused to provide a response:")
        print(math_reasoning.refusal)
    else:
        # Save the reasoning to a Python file
        save_to_file(math_reasoning.parsed)
        
        # Execute the Python file
        print("\nExecuting the generated Python script:")
        execution_output = execute_file("math_reasoning.py")
        print("\nExecution Output:")
        print(execution_output)
