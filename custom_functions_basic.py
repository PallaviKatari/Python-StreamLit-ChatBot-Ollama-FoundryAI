import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Custom Python function
def get_account_balance(account_id: str) -> dict:
    """Return the balance for a sample bank account."""

    # Sample data only
    accounts = {
        "1001": 25000,
        "1002": 48000,
        "1003": 12500
    }

    if account_id not in accounts:
        return {"error": "Account not found"}

    return {
        "account_id": account_id,
        "balance": accounts[account_id],
        "currency": "INR"
    }


def main():
    load_dotenv()

    client = OpenAI(
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY")
    )

    model = os.getenv("MODEL_DEPLOYMENT")

    # 1. Define the custom function tool for the model
    tools = [
        {
            "type": "function",
            "name": "get_account_balance",
            "description": (
                "Get the balance of a bank account "
                "using its account ID."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "account_id": {
                        "type": "string",
                        "description": "The bank account ID"
                    }
                },
                "required": ["account_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    ]

    question = input("Ask a question: ")

    # 2. Send the question and tool definition to the model
    response = client.responses.create(
        model=model,
        input=question,
        tools=tools
    )

    # 3. Check whether the model requested a function call
    for item in response.output:
        if item.type == "function_call":

            print("\nFunction requested:", item.name)
            print("Arguments:", item.arguments)

            if item.name == "get_account_balance":
                args = json.loads(item.arguments)

                # 4. Execute our Python function
                result = get_account_balance(
                    args["account_id"]
                )

                print("Function result:", result)

                # 5. Send the function result back to the model
                response = client.responses.create(
                    model=model,
                    previous_response_id=response.id,
                    input=[
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps(result)
                        }
                    ],
                    tools=tools
                )

                print("\nAssistant:")
                print(response.output_text)
                return

    # No function call was requested
    print("\nAssistant:")
    print(response.output_text)


if __name__ == "__main__":
    main()
