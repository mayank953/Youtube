# calculator_mcp_client_agent.py
from pathlib import Path
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# Define the prompt separately for clarity and reuse
CALCULATOR_MCP_PROMPT = """
You are an intelligent assistant capable of performing various math operations using a connected calculator toolset.

Your tools include:
- `basic_math`: Handles addition, subtraction, multiplication, and division.
- `power`: Calculates exponentiation.
- `modulus`: Computes the remainder of a division operation.
- `square_root`: Returns the square root of a given number.

Usage Principles:
- **Always respond using the appropriate tool** based on user input.
- If user says: "What is 5 plus 3?" → use `basic_math` with operation `add`.
- If user says: "What's 7 raised to the power 2?" → use `power`.
- If user doesn't specify values clearly, ask a short clarifying question.
- **Be concise** in presenting results. Format answer like: "Answer: 64"
- Handle errors gracefully and explain what went wrong.
"""

# Dynamically compute the absolute path to your MCP server
PATH_TO_YOUR_MCP_SERVER_SCRIPT = str((Path(__file__).parent / "server.py").resolve())


# Define the ADK LlmAgent
root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="calculator_mcp_client_agent",
    instruction=CALCULATOR_MCP_PROMPT,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="python3",
                args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT],
            )
            # Optional: you can filter tools like tool_filter=["basic_math"]
        )
    ],
)
