# 🚀 Azure Foundry Agent Demo

A comprehensive guide to using **Azure Foundry AI Projects** with intelligent agents, demonstrating enterprise-grade AI conversational capabilities.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Prerequisites](#prerequisites)
- [Setup & Configuration](#setup--configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**Azure Foundry** (via Azure AI Projects) enables you to build, deploy, and manage intelligent agents with:
- **Conversational AI** powered by enterprise-grade LLMs
- **MCP (Model Context Protocol)** for tool integration and approval workflows
- **Conversation Management** with persistent context
- **Citation & Source Tracking** for reliable information retrieval

The `demo_foundry_iq.py` example demonstrates a **Contoso Product Expert Agent** that can answer questions about outdoor and camping products using Azure-hosted models.

---

## ✨ Key Features

### 1. **Agent-Based Architecture**
- Pre-built agents hosted on Azure Foundry
- Named agent retrieval and instantiation
- Support for agent-specific configurations

### 2. **Conversation Management**
- Persistent conversation threads
- Client-side conversation history tracking
- Conversation context preservation across messages

### 3. **MCP Approval Workflow**
- Tool execution approval requests
- User-controlled tool authorization
- Safe execution of potentially sensitive operations

### 4. **Citation & Sources**
- Automatic source tracking from responses
- Knowledge base reference attribution
- Transparent AI reasoning

### 5. **Azure Identity Integration**
- DefaultAzureCredential for seamless authentication
- Support for multiple credential types (environment, managed identity, CLI)
- No hardcoded API keys required

---

## 📦 Prerequisites

### 1. **Azure Account & Resources**
- Active Azure subscription
- Azure AI Foundry project with deployed agent
- Access to AI Services in your region

### 2. **Python Environment**
- Python 3.9+
- Virtual environment (recommended)

### 3. **Required Packages**

```bash
pip install azure-identity azure-ai-projects python-dotenv
```

### 4. **Environment Variables**
Create a `.env` file in your project root:

```env
# Azure Foundry Configuration
PROJECT_ENDPOINT=https://<your-project>.cognitiveservices.azure.com
AGENT_NAME=your-agent-name

# Azure Credentials (if not using DefaultAzureCredential)
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_TENANT_ID=your-tenant-id
```

---

## 🔧 Setup & Configuration

### Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure Azure Credentials

**Option A: Azure CLI (Recommended for Development)**
```bash
az login
```

**Option B: Environment Variables**
```bash
$env:AZURE_SUBSCRIPTION_ID = "your-subscription-id"
$env:AZURE_TENANT_ID = "your-tenant-id"
```

**Option C: Create Service Principal**
```bash
az ad sp create-for-rbac --name "foundry-demo-sp"
```

### Step 3: Set Environment Variables

Create `.env`:
```env
PROJECT_ENDPOINT=https://your-project.cognitiveservices.azure.com
AGENT_NAME=ProductExpertAgent
```

### Step 4: Verify Configuration

```python
import os
from dotenv import load_dotenv

load_dotenv()
print(f"Endpoint: {os.getenv('PROJECT_ENDPOINT')}")
print(f"Agent: {os.getenv('AGENT_NAME')}")
```

---

## 🎮 Usage

### Basic Example

```python
python demo_foundry_iq.py
```

### Interactive Chat

```
Contoso Product Expert Agent
Ask questions about our outdoor and camping products.
Type 'history' to see conversation history, or 'quit' to exit.

You: What tents do you recommend for beginners?
Agent: I recommend our Alpine Dome Tent...

You: history
# Shows full conversation history

You: quit
# Ends session
```

### Features During Chat

1. **Ask Questions**: Get real-time answers about products
2. **View History**: Type `history` to see the full conversation
3. **Approval Requests**: Some agents may ask for approval before executing tools
4. **Source Citations**: Responses include sources and references

### Handling Approval Requests

When an agent needs approval:

```
[Approval required for: SendEmail]

Server: Product Notification Service
Arguments: {
  "recipient": "user@example.com",
  "subject": "Product Recommendation"
}

Approve this action? (yes/no): yes
```

---

## 🏗️ Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│          Your Python Application                         │
│  (demo_foundry_iq.py)                                    │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  Azure Identity              │
        │  (DefaultAzureCredential)    │
        └──────────────┬───────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│      Azure AI Projects Client                            │
│  • AIProjectClient                                       │
│  • OpenAI Compatibility Layer                            │
└──────────────────┬───────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
   ┌─────────┐           ┌──────────────┐
   │ Agents  │           │ Conversations│
   │ API     │           │ API          │
   └─────────┘           └──────────────┘
        │                     │
        └──────────┬──────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Azure Foundry        │
        │ (Backend Services)   │
        └──────────────────────┘
```

### Data Flow

1. **Initialization**
   - Load environment variables
   - Create Azure credentials
   - Initialize AIProjectClient
   - Retrieve agent by name
   - Create conversation thread

2. **Message Processing**
   - Add user message to conversation
   - Call agent with conversation context
   - Check for approval requests
   - Return response with citations

3. **Response Handling**
   - Extract output text
   - Process citations
   - Update conversation history
   - Display to user

---

## 📚 API Reference

### AIProjectClient

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Initialize client
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://<project>.cognitiveservices.azure.com"
)

# Access sub-clients
agents_client = project_client.agents
openai_client = project_client.get_openai_client()
```

### Agent Operations

```python
# Get agent by name
agent = project_client.agents.get(agent_name="ProductExpertAgent")

# List all agents
agents = project_client.agents.list()

# Get agent properties
print(f"Agent ID: {agent.id}")
print(f"Agent Name: {agent.name}")
```

### Conversation Operations

```python
# Create conversation
conversation = openai_client.conversations.create(items=[])

# Add message to conversation
openai_client.conversations.items.create(
    conversation_id=conversation.id,
    items=[{
        "type": "message",
        "role": "user",
        "content": "Your question here"
    }]
)

# Send response request
response = openai_client.responses.create(
    conversation=conversation.id,
    extra_body={
        "agent_reference": {
            "name": agent.name,
            "type": "agent_reference"
        }
    },
    input=""
)
```

### Response Object

```python
response.output_text        # Main response content
response.citations          # List of sources cited
response.output             # Full output items (including approvals)
```

### MCP Approval Request

```python
# Check for approval request in response
if hasattr(response, 'output') and response.output:
    for item in response.output:
        if hasattr(item, 'type') and item.type == 'mcp_approval_request':
            approval_request = item
            # Handle approval
```

---

## 🔐 Authentication Methods

### 1. **DefaultAzureCredential** (Recommended)
Automatically tries in order:
- Environment variables
- Managed identity (if running in Azure)
- Azure CLI credentials
- Visual Studio credentials
- VS Code credentials
- Interactive browser login

```python
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential(
    exclude_environment_credential=False,
    exclude_managed_identity_credential=True
)
```

### 2. **ClientSecretCredential** (Service Principal)
```python
from azure.identity import ClientSecretCredential

credential = ClientSecretCredential(
    tenant_id=os.getenv("AZURE_TENANT_ID"),
    client_id=os.getenv("AZURE_CLIENT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET")
)
```

### 3. **InteractiveBrowserCredential**
```python
from azure.identity import InteractiveBrowserCredential

credential = InteractiveBrowserCredential()
```

---

## 🐛 Troubleshooting

### Issue: "PROJECT_ENDPOINT and AGENT_NAME must be set"
**Solution**: Ensure `.env` file exists and contains:
```env
PROJECT_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com
AGENT_NAME=YourAgentName
```

### Issue: "Authentication failed"
**Solution**: 
- Run `az login` to authenticate with Azure CLI
- Or set AZURE environment variables
- Check permissions on the agent resource

### Issue: "Agent not found"
**Solution**:
- Verify agent name matches exactly (case-sensitive)
- Ensure agent exists in your Azure Foundry project
- Check subscription and resource group

### Issue: "Connection timeout"
**Solution**:
- Verify PROJECT_ENDPOINT is correct
- Check network connectivity to Azure
- Ensure firewall doesn't block access

### Issue: "Approval request never receives response"
**Solution**:
- Ensure input is 'yes', 'y', 'no', or 'n'
- Check that approval_request_id is correct
- Verify MCP server is accessible

---

## 📊 Example Outputs

### Successful Response with Citations

```
Agent: Our flagship tent is the Alpine Dome Tent. It features:
- 2-person capacity
- 4-season weather protection
- Lightweight design at 2.5kg

Sources:
  - Product Database: tent-001
  - Knowledge Base: camping-essentials
```

### Approval Request Example

```
[Approval required for: SendNotification]

Server: Email Service
Arguments: {
  "recipient": "customer@example.com",
  "template": "product_recommendation",
  "data": {
    "product": "Alpine Dome Tent",
    "discount": "15%"
  }
}

Approve this action? (yes/no): yes
Agent: Notification sent successfully!
```

---

## 🔗 Useful Resources

- [Azure AI Projects Documentation](https://learn.microsoft.com/azure/ai-services/agents/)
- [Azure Identity Documentation](https://learn.microsoft.com/python/api/azure-identity/)
- [OpenAI Python Client](https://github.com/openai/openai-python)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [Azure Foundry Agents SDK](https://learn.microsoft.com/python/api/azure-ai-projects/)

---

## 📝 License

This demo is provided as-is for educational purposes.

---

## 💬 Support

For issues with:
- **Azure Services**: [Azure Support](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade)
- **Python SDK**: [GitHub Issues](https://github.com/Azure/azure-sdk-for-python/issues)
- **Agent Configuration**: Check Azure Foundry project settings

