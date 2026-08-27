import os
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
 
def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
 
    try:
        # Load environment variables
        load_dotenv()
 
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")
 
        if not azure_openai_endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT is not set.")
        if not model_deployment:
            raise ValueError("MODEL_DEPLOYMENT is not set.")
 
        # Initialize the OpenAI client AFTER env vars are loaded
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://ai.azure.com/.default"
        )
 
        openai_client = OpenAI(
            base_url=f"{azure_openai_endpoint}/openai/v1/",
            api_key=token_provider
        )
 
        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue
 
            # Get a response
            completion = openai_client.chat.completions.create(
                model=model_deployment,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant that answers questions and provides information."
                    },
                    {
                        "role": "user",
                        "content": input_text
                    }
                ]
            )
 
            print(completion.choices[0].message.content)
 
    except Exception as ex:
        print(f"Error: {ex}")
 
if __name__ == '__main__':
    main()