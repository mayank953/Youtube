
import asyncio
import json
import logging
import os
from dotenv import load_dotenv

from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

from mcp import types as mcp_types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio

load_dotenv()

# -----------------------------
# 🔧 Logging Setup
# -----------------------------
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "mcp_calc_activity.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE_PATH, mode="w")],
)

# -----------------------------
# 📐 Calculator Tools
# -----------------------------

def basic_math(a: float, b: float, op: str) -> dict:
    """
    Performs a basic arithmetic operation.
    Supported ops: add, subtract, multiply, divide
    """
    try:
        if op == "add":
            return {"success": True, "result": a + b}
        elif op == "subtract":
            return {"success": True, "result": a - b}
        elif op == "multiply":
            return {"success": True, "result": a * b}
        elif op == "divide":
            if b == 0:
                return {"success": False, "message": "Division by zero is not allowed."}
            return {"success": True, "result": a / b}
        else:
            return {"success": False, "message": f"Invalid operation: {op}"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def power(base: float, exponent: float) -> dict:
    """Calculates base raised to the power exponent."""
    try:
        return {"success": True, "result": base ** exponent}
    except Exception as e:
        return {"success": False, "message": str(e)}

def modulus(a: int, b: int) -> dict:
    """Returns a % b."""
    try:
        return {"success": True, "result": a % b}
    except Exception as e:
        return {"success": False, "message": str(e)}

def square_root(x: float) -> dict:
    """Returns the square root of x."""
    try:
        if x < 0:
            return {"success": False, "message": "Square root of negative number not allowed."}
        return {"success": True, "result": x ** 0.5}
    except Exception as e:
        return {"success": False, "message": str(e)}

# -----------------------------
# 🔧 Register ADK Tools
# -----------------------------
ADK_CALC_TOOLS = {
    "basic_math": FunctionTool(
        func=basic_math,
        description="Performs basic arithmetic (add, subtract, multiply, divide)"
    ),
    "power": FunctionTool(
        func=power,
        description="Raises a number to a given power"
    ),
    "modulus": FunctionTool(
        func=modulus,
        description="Computes modulus (a % b)"
    ),
    "square_root": FunctionTool(
        func=square_root,
        description="Returns square root of a number"
    ),
}

# -----------------------------
# 🚀 MCP Server Setup
# -----------------------------
app = Server("multi-tool-calculator")

@app.list_tools()
async def list_mcp_tools() -> list[mcp_types.Tool]:
    """Advertise all available tools."""
    mcp_tool_list = []
    for name, adk_tool in ADK_CALC_TOOLS.items():
        if not adk_tool.name:
            adk_tool.name = name
        mcp_tool = adk_to_mcp_tool_type(adk_tool)
        logging.info(f"Exposing MCP Tool: {mcp_tool.name}")
        mcp_tool_list.append(mcp_tool)
    return mcp_tool_list

@app.call_tool()
async def call_mcp_tool(name: str, arguments: dict) -> list[mcp_types.TextContent]:
    """Dispatch MCP tool call to matching ADK FunctionTool."""
    logging.info(f"Calling MCP Tool: {name} with args: {arguments}")
    if name in ADK_CALC_TOOLS:
        try:
            tool = ADK_CALC_TOOLS[name]
            result = await tool.run_async(arguments, tool_context=None)  # type: ignore
            return [mcp_types.TextContent(type="text", text=json.dumps(result, indent=2))]
        except Exception as e:
            logging.error(f"Error running {name}: {e}", exc_info=True)
            return [mcp_types.TextContent(type="text", text=json.dumps({"success": False, "message": str(e)}))]
    else:
        return [mcp_types.TextContent(type="text", text=json.dumps({
            "success": False,
            "message": f"Tool '{name}' not found"
        }))]

# -----------------------------
# 🧠 MCP Server Execution Logic
# -----------------------------
async def run_mcp_stdio_server():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logging.info("Starting MCP server via stdio")
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    logging.info("MCP Calculator Server launching...")
    try:
        asyncio.run(run_mcp_stdio_server())
    except KeyboardInterrupt:
        logging.info("Server stopped manually.")
    except Exception as e:
        logging.critical(f"Critical server failure: {e}", exc_info=True)
    finally:
        logging.info("MCP Server terminated.")
