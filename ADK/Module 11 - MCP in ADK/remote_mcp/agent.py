import json
import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# https://github.com/modelcontextprotocol/servers

# ✅ Step 1: Get the Tavily API key from env (set it in your .env file)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if TAVILY_API_KEY is None:
    raise ValueError("TAVILY_API_KEY is not set")



# # ✅ Step 2: Build the correct header expected by Tavily MCP
# TAVILY_MCP_HEADERS = json.dumps({
#     "Authorization": f"Bearer {TAVILY_API_KEY}"
# })

# ✅ Step 3: Construct the agent
root_agent = Agent(
    model="gemini-2.0-flash",
    name="Tavily_MCP_Agent",
    instruction="Use Tavily MCP tools to find reliable web results for user queries.",
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=["-y", "tavily-mcp"],
                env={
                    'TAVILY_API_KEY':TAVILY_API_KEY
                },
            )
        )
    ]
)
