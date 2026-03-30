"""Async wrappers around NotebookLMClient for use in the MCP server."""

from __future__ import annotations

from notebooklm import NotebookLMClient


async def get_client() -> NotebookLMClient:
    """Return an authenticated NotebookLMClient using saved storage state."""
    return await NotebookLMClient.from_storage()


async def list_notebooks() -> list[dict]:
    async with await get_client() as client:
        notebooks = await client.notebooks.list()
        return [{"id": nb.id, "title": nb.title} for nb in notebooks]


async def create_notebook(title: str) -> dict:
    async with await get_client() as client:
        nb = await client.notebooks.create(title)
        return {"id": nb.id, "title": nb.title}


async def delete_notebook(notebook_id: str) -> str:
    async with await get_client() as client:
        await client.notebooks.delete(notebook_id)
        return f"Notebook {notebook_id} deleted."


async def add_source_url(notebook_id: str, url: str) -> dict:
    async with await get_client() as client:
        source = await client.sources.add_url(notebook_id, url)
        return {"id": source.id, "title": getattr(source, "title", url)}


async def add_source_text(notebook_id: str, title: str, text: str) -> dict:
    async with await get_client() as client:
        source = await client.sources.add_text(notebook_id, title, text)
        return {"id": source.id, "title": getattr(source, "title", title)}


async def ask_question(notebook_id: str, question: str) -> str:
    async with await get_client() as client:
        result = await client.chat.ask(notebook_id, question)
        return result if isinstance(result, str) else str(result)


async def generate_audio_overview(notebook_id: str) -> dict:
    async with await get_client() as client:
        artifact = await client.artifacts.generate_audio_overview(notebook_id)
        return {"id": artifact.id, "status": getattr(artifact, "status", "pending")}


async def generate_study_guide(notebook_id: str) -> str:
    async with await get_client() as client:
        result = await client.artifacts.generate_study_guide(notebook_id)
        return result if isinstance(result, str) else str(result)
