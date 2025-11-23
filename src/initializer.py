import os

import anthropic
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

# initialize Anthropic model
llm = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# initialize FastMCP server
mcp = FastMCP("research_server")
