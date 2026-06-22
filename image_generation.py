import os
import base64

from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Azure AI Foundry endpoint
endpoint = ""

# Your deployment name
deployment_name = "gpt-image-2"

# Authentication (same as your working script)
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

# Create images folder
os.makedirs("images", exist_ok=True)

image_count = 0

while True:
    prompt = input("\nEnter image prompt (or 'quit' to exit): ").strip()

    if prompt.lower() == "quit":
        print("Exiting...")
        break

    if not prompt:
        print("Please enter a valid prompt.")
        continue

    try:
        print("Generating image...")

        img = client.images.generate(
            model=deployment_name,
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        image_bytes = base64.b64decode(
            img.data[0].b64_json
        )

        image_count += 1
        file_name = f"images/output_{image_count}.png"

        with open(file_name, "wb") as f:
            f.write(image_bytes)

        print(f"Image saved: {file_name}")

    except Exception as ex:
        print(f"Error generating image: {ex}")