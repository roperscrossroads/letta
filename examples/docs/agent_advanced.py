from letta import ChatMemory, EmbeddingConfig, LLMConfig, create_client
from letta.prompts import gpt_system

client = create_client()

# create a new agent
agent_state = client.create_agent(
    name="agent_name",
    memory=ChatMemory(human="Name: Sarah", persona="You are a helpful assistant that loves emojis"),
    llm_config=LLMConfig(
        model="gpt-4",
        model_endpoint_type="openai",
        model_endpoint="https://api.openai.com/v1",
        context_window=8000,
    ),
    embedding_config=EmbeddingConfig(
        embedding_endpoint_type="openai",
        embedding_endpoint="https://api.openai.com/v1",
        embedding_model="text-embedding-ada-002",
        embedding_dim=1536,
        embedding_chunk_size=300,
    ),
    system=gpt_system.get_system_text("memgpt_chat"),
    tools=[],
    include_base_tools=True,
)
print(f"Created agent with name {agent_state.name} and unique ID {agent_state.id}")

# message an agent as a user
response = client.send_message(agent_id=agent_state.id, role="user", message="hello")
print("Usage", response.usage)
print("Agent messages", response.messages)

# message a system message (non-user)
response = client.send_message(agent_id=agent_state.id, role="system", message="[system] user has logged in. send a friendly message.")
print("Usage", response.usage)
print("Agent messages", response.messages)

# delete the agent
client.delete_agent(agent_id=agent_state.id)