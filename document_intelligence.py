import os
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        load_dotenv()
        endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        api_key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

        if not endpoint or not api_key:
            raise ValueError("Missing endpoint or key in .env")

        client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

        file_path = "sample_invoice.pdf"

        # ✅ Correct usage: pass the file stream directly as `body`
        with open(file_path, "rb") as f:
            poller = client.begin_analyze_document(
                model_id="prebuilt-invoice",
                body=f
            )
            result = poller.result()

        print("\n=== Extracted Text ===")
        for page in result.pages:
            for line in page.lines:
                print(line.content)

        print("\n=== Extracted Tables ===")
        for table in result.tables:
            for cell in table.cells:
                print(f"Row {cell.row_index}, Col {cell.column_index}: {cell.content}")

        print("\n=== Key-Value Pairs ===")
        for kv in result.key_value_pairs:
            key = kv.key.content if kv.key else "N/A"
            value = kv.value.content if kv.value else "N/A"
            print(f"{key}: {value}")

    except Exception as ex:
        print(f"Error: {ex}")

if __name__ == "__main__":
    main()
