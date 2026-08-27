from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

knowledge = {
    "hr": [
        "Employees get 20 annual leave days.",
        "Remote work is allowed twice a week."
    ],
    "finance": [
        "Travel reimbursement is capped at $1000.",
        "Expense claims require receipts."
    ],
    "it": [
        "Password resets are done via the Service Desk.",
        "VPN is required for remote access."
    ]
}

question = "How do I reset my password?"

if "leave" in question.lower():
    selected = "hr"

elif "travel" in question.lower() or "expense" in question.lower():
    selected = "finance"

elif "password" in question.lower() or "vpn" in question.lower():
    selected = "it"

else:
    selected = "hr"

context = "\n".join(knowledge[selected])

response = client.responses.create(
    model="gpt-5.1",
    input=f"""
Context:
{context}

Question:
{question}
"""
)

print(response.output_text)