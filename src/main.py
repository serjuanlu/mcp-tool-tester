import asyncio
from mcp_client import MCPClient


async def main():
    client = MCPClient()

    try:
        await client.connect(
            command="python",
            args=["servers/demo_server.py"]
        )

        tools = await client.list_tools()
        print("Tools disponibles:")
        for tool in tools:
            print("-", tool.name)

        result_1 = await client.call_tool("hello", {"name": "Norbert"})
        print("\nResultado hello:")
        print(result_1)

        result_2 = await client.call_tool("add", {"a": 2, "b": 5})
        print("\nResultado add:")
        print(result_2)

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
