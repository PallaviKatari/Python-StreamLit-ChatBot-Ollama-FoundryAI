import os
from dotenv import load_dotenv
from openai import OpenAI

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

    # Get response using the code_interpreter tool
    response = client.responses.create(
        model=model_deployment,
        instructions="You are an AI assistant that provides information. Use the python tool to run code for math problems.",
        input="What is the square root of 16?",
        tools=[{"type": "code_interpreter", "container": {"type": "auto"}}]
    )

    print(response.output_text)

if __name__ == "__main__":
    main()
