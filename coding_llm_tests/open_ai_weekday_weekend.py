import os
import io
import sys
from datetime import datetime
import openai

# Retrieve OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    exit(1)

# Set the OpenAI API key
openai.api_key = api_key

# Function to generate Python code using OpenAI
def generate_code(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        generated_code = response['choices'][0]['message']['content']
        return {"code": generated_code}
    except Exception as e:
        print(f"Error during code generation: {e}")
        exit(1)

# Function to validate and execute the generated code
def validate_and_execute(code_dict):
    captured_output = io.StringIO()
    sys.stdout = captured_output  # Redirect stdout
    try:
        print("Executing Generated Code:")
        print(code_dict["code"])  # Show the code being executed
        exec(code_dict["code"], {})  # Execute the code in a new namespace
        sys.stdout = sys.__stdout__  # Reset stdout
        return {
            "status": "success",
            "code": code_dict["code"],
            "output": captured_output.getvalue()
        }
    except Exception as e:
        sys.stdout = sys.__stdout__  # Reset stdout in case of error
        return {
            "status": "error",
            "error": str(e),
            "code": code_dict["code"]
        }

# Function to analyze results
def analyze_results(output):
    today = datetime.now().strftime("%A")
    is_weekday = today not in ["Saturday", "Sunday"]
    expected_output = (
        "Hello, it’s a weekday" if is_weekday else "Hello, it’s the weekend"
    )
    return expected_output.strip() in output.strip()

# Function to save generated code to a file
def save_code_to_file(code, filename="generated_script.py"):
    with open(filename, "w") as file:
        file.write(code)
    print(f"Generated code has been saved to {filename}")

# Main function
if __name__ == "__main__":
    # Step 1: Generate the Python script
    prompt = (
        "Write a Python script that checks if today is a weekday or weekend. "
        "It should print 'Hello, it’s a weekday' if it’s Monday to Friday, "
        "and 'Hello, it’s the weekend' if it’s Saturday or Sunday."
    )
    generated = generate_code(prompt)
    print("\nGenerated Python Code:")
    print(generated["code"])

    # Save the generated code to a file
    save_code_to_file(generated["code"])

    # Step 2: Validate and execute the generated code
    print("\nValidating and executing the code...")
    result = validate_and_execute(generated)

    # Step 3: Analyze the results
    if result["status"] == "success":
        print("\nCaptured Output from Execution:")
        print(result["output"])
        print("\nAnalyzing Results...")
        is_correct = analyze_results(result["output"])
        if is_correct:
            print("The generated script produced the correct output!")
        else:
            print("The generated script produced incorrect output.")
    else:
        print("\nError occurred during execution:")
        print(result["error"])
