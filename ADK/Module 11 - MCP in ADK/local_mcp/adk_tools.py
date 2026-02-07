
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

from server import basic_math, power, modulus, square_root

ADK_CALC_TOOLS = {
    "basic_math": FunctionTool(
        func=basic_math
    ),
    "power": FunctionTool(
        func=power
    ),
    "modulus": FunctionTool(
        func=modulus
    ),
    "square_root": FunctionTool(
        func=square_root
    ),
}


for k,v in ADK_CALC_TOOLS.items():
    print(f"Registered tool: {k} -> {v.name}")