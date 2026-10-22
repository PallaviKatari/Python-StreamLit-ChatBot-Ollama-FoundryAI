
import sys
import os

from dotenv import load_dotenv
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalysisInput, AnalysisResult
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential


def main():
    # Clear the console
    os.system("cls" if os.name == "nt" else "clear")

    # Load configuration settings
    load_dotenv()

    endpoint = os.getenv("ENDPOINT")
    analyzer_id = os.getenv("ANALYZER")
    api_version = "2025-11-01"

    # Set up Content Understanding client
    credential = DefaultAzureCredential()

    client = ContentUnderstandingClient(
        endpoint=endpoint,
        credential=credential,
        api_version=api_version
    )

    while True:
        file_no = input(
            "\nChoose a file (1, 2, or 3), or anything else to exit: "
        )

        if file_no not in ["1", "2", "3"]:
            break

        file_path = f"images/image{file_no}.png"

        with open(file_path, "rb") as f:
            file_bytes = f.read()

        print(f"Analyzing with {analyzer_id} analyzer...")
        print(f"  File: {file_path}\n")

        # Analyze the file
        try:
            poller = client.begin_analyze(
                analyzer_id=analyzer_id,
                inputs=[
                    AnalysisInput(data=file_bytes)
                ],
            )

            result: AnalysisResult = poller.result()

        except AzureError as err:
            print(f"[Azure Error]: {err}")
            sys.exit(1)

        except Exception as ex:
            print(f"[Unexpected Error]: {ex}")
            sys.exit(1)

        # Display extracted fields
        for field_name, field_data in result.contents[0].fields.items():

            if field_name == "Description":
                print(
                    f"{field_name}:\n"
                    f"{field_data.value_string}\n"
                )

            elif field_name == "Tags":
                print(f"{field_name}:")

                for tag in field_data.value_array:
                    print("  -", tag.value_string)


if __name__ == "__main__":
    main()
