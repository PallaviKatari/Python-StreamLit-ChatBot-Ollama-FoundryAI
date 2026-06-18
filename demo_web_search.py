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

    # Run a web_search query
    response = client.responses.create(
        model=model_deployment,
        input="Search the web for the latest news about generative AI apps.",
        tools=[{"type": "web_search"}]  # <-- web_search tool enabled
    )

    print(response.output_text)

if __name__ == "__main__":
    main()
