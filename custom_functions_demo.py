import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from functions import (
    next_visible_event,
    calculate_observation_cost,
    generate_observation_report,
)

def main():
    # Load environment variables
    load_dotenv()

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    model_deployment = os.getenv("MODEL_DEPLOYMENT")

    if not endpoint or not api_key or not model_deployment:
        raise ValueError("Missing AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, or MODEL_DEPLOYMENT in .env")

    # Connect to your Azure OpenAI resource
    client = OpenAI(base_url=endpoint, api_key=api_key)

    # Define tools
    tools = [
        {
            "type": "function",
            "name": "next_visible_event",
            "description": "Get the next visible event in a given location.",
            "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"]
            }
        },
        {
            "type": "function",
            "name": "calculate_observation_cost",
            "description": "Calculate the cost of an observation based on telescope tier, hours, and priority.",
            "parameters": {
                "type": "object",
                "properties": {
                    "telescope_tier": {"type": "string"},
                    "hours": {"type": "number"},
                    "priority": {"type": "string"}
                },
                "required": ["telescope_tier", "hours", "priority"]
            }
        },
        {
            "type": "function",
            "name": "generate_observation_report",
            "description": "Generate a report summarizing an observation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_name": {"type": "string"},
                    "location": {"type": "string"},
                    "telescope_tier": {"type": "string"},
                    "hours": {"type": "number"},
                    "priority": {"type": "string"},
                    "observer_name": {"type": "string"}
                },
                "required": ["event_name", "location", "telescope_tier", "hours", "priority", "observer_name"]
            }
        }
    ]

    while True:
        user_input = input("\nEnter a prompt (or 'quit' to exit)\nUSER: ").strip()
        if user_input.lower() == "quit":
            break

        # Step 1: Ask the model
        response = client.responses.create(
            model=model_deployment,
            instructions="You are an astronomy assistant. Use the tools when needed.",
            input=user_input,
            tools=tools
        )

        # Step 2: Handle function calls
        input_list = []
        for item in response.output:
            if item.type == "function_call":
                args = json.loads(item.arguments)
                if item.name == "next_visible_event":
                    result = next_visible_event(**args)
                elif item.name == "calculate_observation_cost":
                    result = calculate_observation_cost(**args)
                elif item.name == "generate_observation_report":
                    result = generate_observation_report(**args)
                else:
                    result = "Unknown function."

                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": str(result),
                })

        # Step 3: Send tool results back
        if input_list:
            response = client.responses.create(
                model=model_deployment,
                input=input_list,
                previous_response_id=response.id,
            )

        print(f"\nAGENT: {response.output_text}")

if __name__ == "__main__":
    main()


#What is the next visible event in Europe?
#Calculate the observation cost for a premium telescope, 5 hours, high priority.
#Generate an observation report for the Perseids Meteor Shower in Asia using a standard telescope for 3 hours at medium priority. Observer name: Pallavi.
