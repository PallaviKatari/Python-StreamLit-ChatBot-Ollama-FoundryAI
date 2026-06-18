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

    # Example: search queries restricted to specific bank domains
    bank_queries = [
        "latest updates site:hdfcbank.com",
        "latest updates site:icicibank.com",
        "latest updates site:sbi.co.in",
        "latest updates site:axisbank.com",
        "latest updates site:bankofbaroda.in"
    ]

    for query in bank_queries:
        response = client.responses.create(
            model=model_deployment,
            input=f"Search the web for {query}",
            tools=[{"type": "web_search"}]  # <-- web_search tool enabled
        )
        print(f"\nResults for {query}:\n")
        print(response.output_text)

if __name__ == "__main__":
    main()
