from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load the tokenizer and model
model_name = "Salesforce/codegen-350M-mono"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",  # Automatically map to available hardware (e.g., CPU)
    torch_dtype="auto",  # Use optimal data type
    low_cpu_mem_usage=True  # Optimize memory for CPU
)

# Initialize the pipeline for code generation
code_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto",
    max_length=512  # Limit the output length
)

# Input prompt for code generation
prompt = "Write in Python 3 a Hello World print test."

# Generate code
response = code_pipeline(prompt, max_new_tokens=150, temperature=0.7, top_k=50, top_p=0.9)

# Print the result
print("Generated Code:")
print(response[0]["generated_text"])
