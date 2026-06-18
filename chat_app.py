import os
from dotenv import load_dotenv
from openai import OpenAI

def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Load environment variables
        load_dotenv()

        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        if not endpoint or not api_key or not model_deployment:
            raise ValueError("Missing AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, or MODEL_DEPLOYMENT in .env")

        # Initialize Azure OpenAI client
        openai_client = OpenAI(
            base_url=endpoint,
            api_key=api_key
        )

        while True:
            input_text = input("\nEnter a prompt (or type 'quit' to exit): ").strip()

            if input_text.lower() == "quit":
                break

            if not input_text:
                print("Please enter a prompt.")
                continue

            response = openai_client.chat.completions.create(
                model=model_deployment,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": input_text}
                ]
            )

            print("\nAssistant:")
            print(response.choices[0].message.content)

    except Exception as ex:
        print(f"Error: {ex}")


if __name__ == "__main__":
    main()
