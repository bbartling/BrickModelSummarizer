import os
from openai import OpenAI

# Set the API key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

# Send a chat completion request
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Replace with your model
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ]
)

# Print the full response
print("Full API Response:")
print(response)

# Extract and print the generated message
message_content = response.choices[0].message.content
print("\nGenerated Content:")
print(message_content)
