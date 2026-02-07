from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

ollama_model = LiteLlm(model='ollama_chat/llama3.2')

# It is important to set the provider ollama_chat instead of ollama. Using ollama will result in unexpected behaviors such as infinite tool call loops and ignoring previous context.


# export OLLAMA_API_BASE="http://localhost:11434"
# adk web

root_agent = Agent(
    model=ollama_model,
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
