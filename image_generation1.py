import os
import base64
from openai import OpenAI

# Azure AI Foundry endpoint
endpoint = ""

# Your deployment name
deployment_name = "gpt-image-2"

# Replace with your actual API key
api_key = ""

# Initialize client with API key
client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

# Create images folder
os.makedirs("images", exist_ok=True)
image_count = 0

# Generate one image (example prompt)
prompt = "A cute baby polar bear"
print("Generating image...")

img = client.images.generate(
    model=deployment_name,
    prompt=prompt,
    n=1,
    size="1024x1024",
)

# Decode base64 image
image_bytes = base64.b64decode(img.data[0].b64_json)

# Save into images folder with incremented filename
image_count += 1
file_name = f"images/output1_{image_count}.png"

with open(file_name, "wb") as f:
    f.write(image_bytes)

print(f"Image saved: {file_name}")
