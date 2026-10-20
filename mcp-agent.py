import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool
from openai.types.responses.response_input_param import (
    McpApprovalResponse,
    ResponseInputParam,
)


def main():
    # Load environment variables from the .env file
    load_dotenv()

    project_endpoint = os.getenv("FOUNDRY_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT")

    if not project_endpoint or not model_deployment:
        raise ValueError(
            "Please set PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME "
            "in your .env file."
        )

    # Connect to the Azure AI Foundry project
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(
            endpoint=project_endpoint,
            credential=credential,
        ) as project_client,
        project_client.get_openai_client() as openai_client,
    ):
        # Initialize the MCP tool
        mcp_tool = MCPTool(
            server_label="api-specs",
            server_url="https://learn.microsoft.com/api/mcp",
            require_approval="always",
        )

        # Create a new agent with the MCP tool
        agent = project_client.agents.create_version(
            agent_name="MyAgent",
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions=(
                    "You are a helpful agent that can use MCP tools "
                    "to assist users. Use the available MCP tools to "
                    "answer questions and perform tasks."
                ),
                tools=[mcp_tool],
            ),
        )

        print(
            f"Agent created "
            f"(id: {agent.id}, name: {agent.name}, "
            f"version: {agent.version})"
        )

        try:
            # Create a conversation
            conversation = openai_client.conversations.create()

            print(f"Created conversation (id: {conversation.id})")

            # Send the initial request
            response = openai_client.responses.create(
                conversation=conversation.id,
                input=(
                    "Give me the Azure CLI commands to create an "
                    "Azure Container App with a managed identity."
                ),
                extra_body={
                    "agent_reference": {
                        "name": agent.name,
                        "type": "agent_reference",
                    }
                },
            )

            # Process MCP approval requests
            while True:
                input_list: ResponseInputParam = []

                for item in response.output:
                    if item.type == "mcp_approval_request":
                        if item.server_label == "api-specs" and item.id:
                            # Automatically approve the MCP request
                            input_list.append(
                                McpApprovalResponse(
                                    type="mcp_approval_response",
                                    approve=True,
                                    approval_request_id=item.id,
                                )
                            )

                # Stop when there are no more approval requests
                if not input_list:
                    break

                # Submit approvals and retrieve the next response
                response = openai_client.responses.create(
                    input=input_list,
                    previous_response_id=response.id,
                    extra_body={
                        "agent_reference": {
                            "name": agent.name,
                            "type": "agent_reference",
                        }
                    },
                )

            # Display the final agent response
            print(f"\nAgent response:\n{response.output_text}")

        finally:
            # Delete the agent version
            project_client.agents.delete_version(
                agent_name=agent.name,
                agent_version=agent.version,
            )

            print("Agent deleted")


if __name__ == "__main__":
    main()
