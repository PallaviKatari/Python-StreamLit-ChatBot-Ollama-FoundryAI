from azure.ai.foundry import Agent, AgentThread

# Step 1: Define agents with roles
researcher = Agent(
    name="Researcher",
    instructions="Gather factual information from trusted sources."
)

analyst = Agent(
    name="Analyst",
    instructions="Interpret the data and highlight key insights."
)

summarizer = Agent(
    name="Summarizer",
    instructions="Condense the discussion into a clear summary."
)

# Step 2: Create a Group Chat orchestration thread
thread = AgentThread(pattern="group_chat")

# Step 3: Add agents to the thread
thread.add_agent(researcher)
thread.add_agent(analyst)
thread.add_agent(summarizer)

# Step 4: Run the group chat
result = thread.run("Discuss the impact of renewable energy adoption on global markets")

# Step 5: Output the result
print(result)
