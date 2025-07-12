# AI Code Companion

A Streamlit-based AI coding assistant with Firebase integration and Ollama support.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

## Features

- 🔐 Firebase Authentication
- 💬 Chat-based AI assistance
- 🤖 Ollama integration for local LLM
- 💾 Persistent chat history
- 🎨 Modern dark theme UI

## Security

- Firebase credentials are stored in environment variables
- `.env` files are automatically ignored by git
- Never commit sensitive credentials to version control

## MCP Server Setup

To run the MCP server in your local system:

1. Install uv (python package manager)
2. `uv init .`
3. `uv add "mcp[cli]"`
4. `uv run mcp install <mcp_file_name.py>`
