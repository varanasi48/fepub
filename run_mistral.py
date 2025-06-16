import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key = "emprhvoUjSVxekhAMwiLzSapRVcZjNht"
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

messages = [ChatMessage(role="user", content="Who is the best French painter? Answer in one short sentence.")]
tools = []  # Define your tools here if needed

response = client.chat(
    model=model,
    messages=messages,
    tools=tools,
    max_tokens=2000,
    
)

print(response)