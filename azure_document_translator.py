import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

SUBSCRIPTION_KEY = os.getenv("AZURE_OPENAI_API_KEY")

# Azure Translator endpoint
endpoint = ""

url = f"{endpoint}/translator/document:translate"

# Request headers
headers = {
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
}

# Translation parameters
params = {
    "sourceLanguage": "en",
    "targetLanguage": "fr",
    "api-version": "2024-05-01"
}

# Input and output files
input_file = Path("./data/events.txt")
output_file = Path("./data/events_translated.txt")

def main():
    if not SUBSCRIPTION_KEY:
        print("ERROR: AZURE_TRANSLATOR_KEY is missing from .env")
        return

    if not input_file.exists():
        print(f"ERROR: Input file not found: {input_file.resolve()}")
        return

    try:
        with input_file.open("rb") as document:
            files = {
                "document": (
                    input_file.name,
                    document,
                    "text/plain"
                )
            }

            print("Sending document for translation...")

            response = requests.post(
                url,
                headers=headers,
                files=files,
                params=params,
                timeout=120
            )

        print("HTTP Status Code:", response.status_code)

        if response.status_code == 200:
            output_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            output_file.write_bytes(response.content)

            print("Translation successful!")
            print(f"Translated file saved to: {output_file.resolve()}")
            print("Translated content:")

            print(
                response.content.decode("utf-8-sig", errors="replace")
            )

        else:
            print("Translation failed.")
            print("Response:", response.text)

    except requests.exceptions.RequestException as error:
        print("HTTP request error:", error)

    except OSError as error:
        print("File error:", error)


if __name__ == "__main__":
    main()
