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
        model_deployment = os.getenv("MODEL_NAME1")   # e.g., gpt-4o-transcribe
        api_key = os.getenv("AZURE_OPENAI_API_KEY")   # store your key in .env
        file_path = Path(__file__).parent / "20261021085834_b6a822d5.mp3"
        
        # Play the speech file
        playsound(file_path)
        
        # Create the Azure OpenAI client using API key
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version="2025-03-01-preview"
        )

        # Call model to transcribe audio file
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=model_deployment,
                file=audio_file,
                response_format="text"
            )

        print(transcription)

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
