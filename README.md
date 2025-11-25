# MCP Project

### Find pre-built servers:
- link: https://github.com/modelcontextprotocol/servers
---

### Pre-requisites:
- uv (https://docs.astral.sh/uv/) package manager
- Node.js installed on your system
---
### Virtual Environment:
- Navigate to the project directory and initiate it with `uv`:
    - `cd <target_directory>`
    - `uv init`

- Create virtual environment and activate it:
    - `uv venv`
    - `.venv/Scripts/activate`

- Install dependencies:
    - `uv add -r requirements.txt`

### Launch MCP inspector (sandbox to play around):
```bash
npx @modelcontextprotocol/inspector uv run src/research_server.py
```



