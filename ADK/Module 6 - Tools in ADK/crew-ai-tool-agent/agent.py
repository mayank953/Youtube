from google.adk.agents import Agent
import os
import dotenv
from google.adk.tools.crewai_tool import CrewaiTool
from crewai_tools import SerperDevTool
dotenv.load_dotenv()



SERPER_API_KEY = os.getenv('SERPER_API_KEY')
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY environment variable is not set.")

serper_crewai_tool = SerperDevTool(
    country="in",
    locale="in",
    location="Mumbai, Maharashtra, India",
    n_results=10,
)

adk_serper_tool = CrewaiTool(
    name = 'InternetNewsSearch',
    description= 'Search the internet for news articles and information using Serper',
    tool = serper_crewai_tool,
)

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='A helpful assistant for user questions.',
    tools = [adk_serper_tool],
    instruction='You are a helpful assistant. Answer user questions and use the tools provided when necessary.',
)
