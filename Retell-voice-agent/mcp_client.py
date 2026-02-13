"""Utility helpers for working with the Retell AI MCP server via Python.

Usage:
    $ export RETELL_API_KEY=...
    $ python -m Retell-voice-agent.mcp_client list-tools

The module exposes a small CLI so you can quickly sanity-check your
connection, dump the available tools, and inspect the agents that the
Retell AI MCP server exposes.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
from contextlib import asynccontextmanager
from typing import Any, Dict

import dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

PACKAGE_NAME = "@abhaybabbar/retellai-mcp-server"

dotenv.load_dotenv()

def resolve_npx_path() -> str:
    """Return the absolute path to the `npx` executable.

    The notebook kernel does not inherit your interactive login shell, so the
    `PATH` that normally exposes `npx` is often missing. Resolving it ahead of
    time avoids the FileNotFoundError you were seeing.
    """
    npx_path = shutil.which("npx")
    if npx_path:
        return npx_path

    fallback = "/home/hex/.nvm/versions/node/v24.12.0/bin/npx"
    if os.path.exists(fallback):
        return fallback

    raise FileNotFoundError(
        "Could not find `npx`. Install Node.js (https://nodejs.org/) or update PATH"
    )

def build_server_params() -> StdioServerParameters:
    api_key = os.getenv("RETELL_API_KEY")
    if not api_key:
        raise RuntimeError("RETELL_API_KEY is missing. Add it to .env or export it in your shell.")

    env = dict(os.environ)
    env["RETELL_API_KEY"] = api_key

    return StdioServerParameters(
        command=resolve_npx_path(),
        args=["-y", PACKAGE_NAME],
        env=env,
    )

@asynccontextmanager
def retell_session():
    params = build_server_params()
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session

def extract_text_content(result) -> str:
    parts = []
    for item in getattr(result, "content", []) or []:
        text = getattr(item, "text", None)
        if text:
            parts.append(text)
    return "\n".join(parts)

async def list_tools() -> None:
    async with retell_session() as session:
        response = await session.list_tools()
        print("\n=== Retell AI MCP Tools ===")
        for tool in response.tools:
            print(f"- {tool.name}: {tool.description}")
        print("===========================\n")

async def list_agents() -> None:
    async with retell_session() as session:
        try:
            result = await session.call_tool("list_agents", arguments={})
        except Exception as exc:  # noqa: BLE001 - surface server errors cleanly
            raise RuntimeError("The MCP server does not expose a `list_agents` tool") from exc

        payload = extract_text_content(result)
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            data = payload

        print("\n=== Retell Voice Agents ===")
        print(json.dumps(data, indent=2) if isinstance(data, (dict, list)) else data)
        print("===========================\n")

async def create_agent(agent_payload: Dict[str, Any]) -> None:
    async with retell_session() as session:
        result = await session.call_tool("create_agent", arguments=agent_payload)
        payload = extract_text_content(result)
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            data = payload
        print(json.dumps(data, indent=2) if isinstance(data, (dict, list)) else data)

def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Interact with Retell AI MCP server")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-tools", help="List MCP tools exposed by the server")
    sub.add_parser("list-agents", help="List available voice agents")

    create_cmd = sub.add_parser("create-agent", help="Create a Retell AI voice agent")
    create_cmd.add_argument("payload", help="Path to a JSON file describing the agent")

    return parser

def main() -> None:
    parser = _build_cli()
    args = parser.parse_args()

    if args.command == "list-tools":
        asyncio.run(list_tools())
    elif args.command == "list-agents":
        asyncio.run(list_agents())
    elif args.command == "create-agent":
        with open(args.payload, "r", encoding="utf-8") as fp:
            payload = json.load(fp)
        asyncio.run(create_agent(payload))

if __name__ == "__main__":
    main()
