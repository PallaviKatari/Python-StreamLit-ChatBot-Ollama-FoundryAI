import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
model_deployment = os.getenv("MODEL_DEPLOYMENT")

if not endpoint or not api_key or not model_deployment:
    raise ValueError("Missing AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, or MODEL_DEPLOYMENT in .env")

# Connect to your Azure OpenAI resource
client = OpenAI(base_url=endpoint, api_key=api_key)

# Local demo dataset
def custom_search(query: str) -> str:
    knowledge_base = {
        "leave policy": "Employees are entitled to 20 days of paid leave per year.",
        "work hours": "Standard work hours are 9 AM to 6 PM, Monday to Friday.",
        "remote work": "Remote work is allowed up to 2 days per week."
    }
    result = knowledge_base.get(query.lower(), "No information found.")
    return json.dumps({"query": query, "result": result})

# Register the tool
tools = [
    {
        "type": "function",
        "name": "custom_search",
        "description": "Search a custom HR knowledge base.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    }
]

# Step 1: Ask the model a question
response = client.responses.create(
    model=model_deployment,
    instructions="You are an assistant that answers HR policy questions using the custom_search tool.",
    input="What is the leave policy?",
    tools=tools
)

# Step 2: Handle function call
input_list = []
for item in response.output:
    if item.type == "function_call" and item.name == "custom_search":
        args = json.loads(item.arguments)
        result = custom_search(**args)
        input_list.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": result,
        })

# Step 3: Send function output back to the model
if input_list:
    response = client.responses.create(
        model=model_deployment,
        input=input_list,
        previous_response_id=response.id,
    )

# Final answer
print("AGENT:", response.output_text)
