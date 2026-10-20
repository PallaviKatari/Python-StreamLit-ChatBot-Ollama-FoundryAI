# import os
# from dotenv import load_dotenv
# from openai import OpenAI

# def main():
#     # Clear the console
#     os.system('cls' if os.name == 'nt' else 'clear')

#     try:
#         # Load environment variables
#         load_dotenv()

#         endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
#         api_key = os.getenv("AZURE_OPENAI_API_KEY")
#         model_deployment = os.getenv("MODEL_DEPLOYMENT")

#         if not endpoint or not api_key or not model_deployment:
#             raise ValueError("Missing AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, or MODEL_DEPLOYMENT in .env")

#         # Initialize Azure OpenAI client
#         client1 = OpenAI(
#             base_url=endpoint,
#             api_key=api_key
#         )

#         while True:
#             input_text = input("\nEnter a prompt (or type 'quit' to exit): ").strip() # What is LLM?

#             if input_text.lower() == "quit":
#                 break

#             if not input_text:
#                 print("Please enter a prompt.")
#                 continue

#             # Responses and Chat Completions
#             # client.responses.create()
#             # Stateful - array of messages
#             response1 = client1.chat.completions.create(
#                 model=model_deployment, #gpt-5.6-sol
#                 messages=[
#                     {"role": "system", "content": "You are a helpful AI assistant."},
#                     {"role": "user", "content": input_text} #What is LLM?
#                 ]
#             )

#             print("\nAssistant:")
#             print(response1.choices[0].message.content)

#     except Exception as ex:
#         print(f"Error: {ex}")


# if __name__ == "__main__":
#     main()

import os
from dotenv import load_dotenv
from openai import OpenAI


def main():
    os.system("cls" if os.name == "nt" else "clear")

    try:
        # Load environment variables
        load_dotenv()

        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        if not endpoint or not api_key or not model_deployment:
            raise ValueError(
                "Missing AZURE_OPENAI_ENDPOINT, "
                "AZURE_OPENAI_API_KEY, or MODEL_DEPLOYMENT in .env"
            )

        # Initialize the Azure OpenAI-compatible client
        client = OpenAI(
            base_url=endpoint,
            api_key=api_key
        )

        print("Azure OpenAI Chatbot - Responses API")
        print("Type 'quit' to exit.\n")

        previous_response_id = None

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            if not user_input:
                print("Please enter a prompt.")
                continue

            # Prepare the request
            request = {
                "model": model_deployment,
                "instructions": "You are a helpful AI assistant.",
                "input": user_input #What is AI?
            }

            # Continue the conversation when a previous response exists
            if previous_response_id:
                request["previous_response_id"] = previous_response_id

            # Call the Responses API
            response = client.responses.create(**request)

            print("\nAssistant:")
            print(response.output_text)
            print()

            # Save the response ID for the next turn
            previous_response_id = response.id

    except Exception as ex:
        print(f"Error: {ex}")


if __name__ == "__main__":
    main()
