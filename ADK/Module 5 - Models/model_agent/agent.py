from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import dotenv
dotenv.load_dotenv()
import os
from google.genai.types import GenerateContentConfig 


api_key = os.getenv('OPENAI_API_KEY')

model_openAI = LiteLlm(model="openai/gpt-4o",
                       api_key=api_key,
                       temperature=0.7,
                       max_tokens=10, # https://docs.litellm.ai/docs/completion/input
                       )

root_agent = Agent(
    model=model_openAI,
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
