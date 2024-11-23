import io
import sys
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load the tokenizer and model
model_name = "Salesforce/codegen-350M-mono"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype="auto",
    low_cpu_mem_usage=True,
)

# Initialize the pipeline for code generation
code_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto",
    max_length=512
)

# Function to generate Python code
def generate_code(prompt):
    response = code_pipeline(prompt, max_new_tokens=150, temperature=0.7, top_k=50, top_p=0.9)
    generated_code = response[0]["generated_text"]
    return {"code": generated_code}

# Function to validate and execute the generated code
def validate_and_execute(code_dict):
    captured_output = io.StringIO()
    sys.stdout = captured_output  # Redirect stdout
    try:
        print("Executing Generated Code:")
        print(code_dict["code"])  # Show the code being executed
        exec(code_dict["code"])  # Execute the code
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
