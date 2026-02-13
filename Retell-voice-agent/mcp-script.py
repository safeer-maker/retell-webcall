import dotenv, os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

dotenv.load_dotenv()  # Load environment variables from .env file


async def test_retell_mcp():
    # 1. Define the server parameters (matching your JSON config)
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@abhaybabbar/retellai-mcp-server"],
        env={
            "RETELL_API_KEY": os.getenv("RETELL_API_KEY", "YOUR_RETELL_API_KEY_HERE"),
            "PATH": "/usr/local/bin:/usr/bin:/bin" # Ensure npx is in the path
        }
    )

    print("🚀 Connecting to Retell AI MCP Server...")

    # 2. Start the server and create a session
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # 3. List available tools (to see what's available)
            print("\n--- Available Tools ---")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"Tool: {tool.name} - {tool.description}")

            # 4. Example: Access your Voice Agents
            # The tool name usually matches 'list_agents' or similar in this server
            print("\n--- Fetching Voice Agents ---")
            try:
                # We call the tool by name. Note: check the tool list output 
                # above to confirm the exact name (e.g., "list_agents")
                result = await session.call_tool("list_agents", arguments={})
                print("Result:", result.content[0].text)
            except Exception as e:
                print(f"❌ Error calling tool: {e}")

if __name__ == "__main__":
    asyncio.run(test_retell_mcp())