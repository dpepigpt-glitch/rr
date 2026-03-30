"""MCP server exposing NotebookLM capabilities to Claude."""

from __future__ import annotations

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

import notebooklm_claude.tools as nlm

app = Server("notebooklm")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_notebooks",
            description="List all notebooks in NotebookLM.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="create_notebook",
            description="Create a new notebook in NotebookLM.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title for the new notebook"},
                },
                "required": ["title"],
            },
        ),
        types.Tool(
            name="delete_notebook",
            description="Delete a notebook by its ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "notebook_id": {"type": "string", "description": "ID of the notebook to delete"},
                },
                "required": ["notebook_id"],
            },
        ),
        types.Tool(
            name="add_source_url",
            description="Add a URL (webpage, YouTube video, etc.) as a source to a notebook.",
            inputSchema={
                "type": "object",
                "properties": {
                    "notebook_id": {"type": "string", "description": "Target notebook ID"},
                    "url": {"type": "string", "description": "URL to add as a source"},
                },
                "required": ["notebook_id", "url"],
            },
        ),
        types.Tool(
            name="add_source_text",
            description="Add raw text as a source to a notebook.",
            inputSchema={
                "type": "object",
                "properties": {
                    "notebook_id": {"type": "string", "description": "Target notebook ID"},
                    "title": {"type": "string", "description": "Title for this text source"},
                    "text": {"type": "string", "description": "Text content to add"},
                },
                "required": ["notebook_id", "title", "text"],
            },
        ),
        types.Tool(
            name="ask_question",
            description="Ask a question about a notebook's content and get an AI-generated answer.",
            inputSchema={
                "type": "object",
                "properties": {
                    "notebook_id": {"type": "string", "description": "Notebook ID to query"},
                    "question": {"type": "string", "description": "Question to ask"},
                },
                "required": ["notebook_id", "question"],
            },
        ),
        types.Tool(
            name="generate_audio_overview",
            description="Generate an Audio Overview (podcast-style summary) for a notebook.",
            inputSchema={
                "type": "object",
                "properties": {
                    "notebook_id": {"type": "string", "description": "Notebook ID"},
                },
                "required": ["notebook_id"],
            },
        ),
        types.Tool(
            name="generate_study_guide",
            description="Generate a study guide for a notebook.",
            inputSchema={
                "type": "object",
                "properties": {
                    "notebook_id": {"type": "string", "description": "Notebook ID"},
                },
                "required": ["notebook_id"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        if name == "list_notebooks":
            result = await nlm.list_notebooks()
        elif name == "create_notebook":
            result = await nlm.create_notebook(arguments["title"])
        elif name == "delete_notebook":
            result = await nlm.delete_notebook(arguments["notebook_id"])
        elif name == "add_source_url":
            result = await nlm.add_source_url(arguments["notebook_id"], arguments["url"])
        elif name == "add_source_text":
            result = await nlm.add_source_text(
                arguments["notebook_id"], arguments["title"], arguments["text"]
            )
        elif name == "ask_question":
            result = await nlm.ask_question(arguments["notebook_id"], arguments["question"])
        elif name == "generate_audio_overview":
            result = await nlm.generate_audio_overview(arguments["notebook_id"])
        elif name == "generate_study_guide":
            result = await nlm.generate_study_guide(arguments["notebook_id"])
        else:
            raise ValueError(f"Unknown tool: {name}")

        text = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False, indent=2)
        return [types.TextContent(type="text", text=text)]

    except Exception as exc:
        return [types.TextContent(type="text", text=f"Error: {exc}")]


def main() -> None:
    asyncio.run(_run())


async def _run() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    main()
