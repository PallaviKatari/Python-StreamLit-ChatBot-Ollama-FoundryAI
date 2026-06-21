from dotenv import load_dotenv
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

def main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')
        agent_name = os.getenv('AGENT_NAME')
        
        project_client = AIProjectClient(
            endpoint=foundry_endpoint,
            credential=DefaultAzureCredential(),
        )

        # Get an OpenAI client
        openai_client = project_client.get_openai_client()
        
        # Use the agent to get a response
        prompt = input("User prompt: ")
        response = openai_client.responses.create(
         input=[{"role": "user", "content": prompt}],
            extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
        )

        print(f"{agent_name}: {response.output_text}")

        # Uncomment for full JSON
        # print(response.model_dump_json(indent=2))
        
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()

#Extract named entities from the following text: "Pierre and I went to Paris on July 14th."

#UnComment print(f"\nResponse Details: {response.model_dump_json(indent=2)}") and rerun
#Tell me what entities and dates are mentioned in this review, and whether it is positive or negative: "I booked my flight to Paris in July with Margie's Travel, and it was fantastic!"