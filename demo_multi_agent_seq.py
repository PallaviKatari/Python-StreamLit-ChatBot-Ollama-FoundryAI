import asyncio
from typing import cast
from dotenv import load_dotenv
#pip install agent-framework
#   or
#pip install agent-framework==1.0.0rc3 or pip install agent-framework==1.0.0rc3 --use-deprecated=legacy-resolver

#pip install opentelemetry-semantic-conventions

#If pip complains about depth, add lower bounds for dependencies
#python -m pip install --upgrade pip setuptools wheel
#pip install agent-framework==1.0.0rc3 --use-deprecated=legacy-resolver
# OR
#pip install "agent-framework==1.0.0rc3" "httpx>=0.24.0" "pydantic>=2.0.0"


import asyncio
from typing import cast
from dotenv import load_dotenv

from agent_framework import Message
from agent_framework.azure_ai import AzureAIAgentClient   # ✅ correct import for 1.9.0
from agent_framework.orchestrations import SequentialBuilder
from azure.identity import AzureCliCredential

# Load environment variables
load_dotenv()

async def main():
    summarizer_instructions = """
    Summarize the customer's feedback in one short sentence. Keep it neutral and concise.
    Example output:
    App crashes during photo upload.
    User praises dark mode feature.
    """

    classifier_instructions = """
    Classify the feedback as one of the following: Positive, Negative, or Feature request.
    """

    action_instructions = """
    Based on the summary and classification, suggest the next action in one short sentence.
    Example output:
    Escalate as a high-priority bug for the mobile team.
    Log as positive feedback to share with design and marketing.
    Log as enhancement request for product backlog.
    """

    credential = AzureCliCredential()
    async with AzureAIAgentClient(credential=credential) as chat_client:
        summarizer = chat_client.as_agent(instructions=summarizer_instructions, name="summarizer")
        classifier = chat_client.as_agent(instructions=classifier_instructions, name="classifier")
        action = chat_client.as_agent(instructions=action_instructions, name="action")

        feedback = """
        I use the dashboard every day to monitor metrics, and it works well overall.
        But when I'm working late at night, the bright screen is really harsh on my eyes.
        If you added a dark mode option, it would make the experience much more comfortable.
        """

        workflow = SequentialBuilder(participants=[summarizer, classifier, action]).build()

        outputs: list[list[Message]] = []
        async for event in workflow.run(f"Customer feedback: {feedback}", stream=True):
            if event.type == "output":
                outputs.append(cast(list[Message], event.data))

        if outputs:
            for i, msg in enumerate(outputs[-1], start=1):
                name = msg.author_name or ("assistant" if msg.role == "assistant" else "user")
                print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")

if __name__ == "__main__":
    asyncio.run(main())
