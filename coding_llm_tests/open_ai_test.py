import os
import openai

# Retrieve OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    exit(1)

# Set the OpenAI API key
openai.api_key = api_key

# Generate text using GPT-3.5 Turbo
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Write a Python script that prints 'Hello, World!'."}],
    max_tokens=100,
    temperature=0.7
)

# Print the generated text
print("Generated Text:")
print(response['choices'][0]['message']['content'])
