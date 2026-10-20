import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    model_deployment = os.getenv("MODEL_DEPLOYMENT")
    vector_store_id = os.getenv("VECTOR_STORE_ID")

    if not endpoint or not api_key or not model_deployment:
        raise ValueError("Check your Azure settings in .env")

    client = OpenAI(
        base_url=endpoint,
        api_key=api_key
    )

    # Step 1: Create a vector store if one is not configured.
    if not vector_store_id:
        vector_store = client.vector_stores.create(
            name="Bank Knowledge Base"
        )
        vector_store_id = vector_store.id
        print("Created vector store:", vector_store_id)

        print(
            "\nSave this ID as VECTOR_STORE_ID in your .env "
            "to reuse the same knowledge base."
        )

    # Step 2: Upload the sample document.
    file_path = Path("documents/bank_policy.txt")

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with file_path.open("rb") as file:
        uploaded_file = client.files.create(
            file=file,
            purpose="assistants"
        )

    print("Uploaded file:", uploaded_file.id)

    # Step 3: Attach the uploaded file to the vector store.
    vector_file = client.vector_stores.files.create(
        vector_store_id=vector_store_id,
        file_id=uploaded_file.id
    )

    print("Indexing status:", vector_file.status)

    # Step 4: Wait until the document is indexed.
    while vector_file.status in ("in_progress", "queued"):
        time.sleep(2)

        vector_file = client.vector_stores.files.retrieve(
            vector_store_id=vector_store_id,
            file_id=uploaded_file.id
        )

        print("Indexing status:", vector_file.status)

    if vector_file.status != "completed":
        raise RuntimeError(
            f"File indexing failed: {vector_file.status}"
        )

    # Step 5: Ask a question using file_search.
    question = (
        "According to the uploaded policy, "
        "what should customers do if an unauthorized "
        "transaction occurs?"
    )

    response = client.responses.create(
        model=model_deployment,
        input=question,
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [vector_store_id],
                "max_num_results": 3
            }
        ],
        include=["file_search_call.results"]
    )

    print("\nQuestion:", question)
    print("\nAnswer:\n")
    print(response.output_text)

    # Step 6: Display retrieved passages, if available.
    for item in response.output:
        if item.type == "file_search_call":
            print("\nFile search queries:", item.queries)

            for result in item.results or []:
                print("\nRetrieved file:", result.filename)
                print("Relevant passage:", result.text)


if __name__ == "__main__":
    main()
