import os
from pathlib import Path
from playsound3 import playsound
from dotenv import load_dotenv

# Import namespaces
from openai import AzureOpenAI

def main():
    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get Configuration Settings
        load_dotenv()
        endpoint = os.getenv("FOUNDRY_ENDPOINT")
        model_deployment = os.getenv("MODEL_NAME")   # e.g., gpt-4o-mini-tts
        api_key = os.getenv("AZURE_OPENAI_API_KEY")  # store your key in .env
        speech_file_path = Path(__file__).parent / "kpmg.mp3"

        # Create the Azure OpenAI client using API key
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version="2025-03-01-preview"
        )

        # Generate speech and save to file
        with client.audio.speech.with_streaming_response.create(
            model=model_deployment,
            voice="alloy",
            input="Hi KPMG Participants.. Welcome to the Azure AI Foundry demo. This is a text-to-speech example using the OpenAI API.",
            instructions="Speak in a serious tone.",
        ) as response:
            response.stream_to_file(speech_file_path)

        # Play the generated speech file
        playsound(speech_file_path)

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
