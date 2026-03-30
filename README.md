# notebooklm-claude

MCP server that integrates [Google NotebookLM](https://notebooklm.google.com) with Claude Code (and any MCP-compatible Claude client).

Powered by [notebooklm-py](https://github.com/teng-lin/notebooklm-py) — unofficial Python API for NotebookLM.

## What this does

Exposes NotebookLM as a set of Claude tools via the [Model Context Protocol (MCP)](https://modelcontextprotocol.io). Once configured, Claude can:

- List, create, and delete notebooks
- Add URLs, YouTube videos, or raw text as sources
- Ask questions about notebook content
- Generate Audio Overviews and study guides

## Installation

```bash
pip install -e ".[browser]"
# or: pip install notebooklm-py[browser] mcp
```

> Requires Python 3.11+ and a Google account with NotebookLM access.

## Setup

### 1. Authenticate with Google

```bash
notebooklm login
```

This opens a browser for Google login and saves the session locally.

### 2. Configure Claude Code

The `.claude/settings.json` in this repo already registers the MCP server. Start Claude Code from this directory and the `notebooklm:*` tools will be available automatically.

Alternatively, add this to your global `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "python",
      "args": ["-m", "notebooklm_claude.server"]
    }
  }
}
```

## Usage with Claude

Once the MCP server is running, ask Claude naturally:

```
Create a new notebook called "AI Research"
Add https://arxiv.org/abs/2310.06825 as a source to notebook <id>
Ask the notebook: what are the main findings?
Generate a study guide for notebook <id>
```

## Available tools

| Tool | Description |
|------|-------------|
| `list_notebooks` | List all your NotebookLM notebooks |
| `create_notebook` | Create a new notebook |
| `delete_notebook` | Delete a notebook by ID |
| `add_source_url` | Add a URL (webpage, YouTube, etc.) as a source |
| `add_source_text` | Add raw text as a source |
| `ask_question` | Ask a question about notebook content |
| `generate_audio_overview` | Generate an Audio Overview (podcast-style) |
| `generate_study_guide` | Generate a study guide |

## Notes

- Uses undocumented Google APIs — may break without notice
- Not for production use; best for personal research workflows
- Run `notebooklm login` again if you get authentication errors
