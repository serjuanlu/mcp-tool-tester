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

        result_2 = await client.call_tool("add", {"a": 3, "b": 5})
        print("\nResultado add:")
        print(result_2)

        files = await client.call_tool("list_files", {"directory": "."})
        print("\nArchivos en el proyecto:")
        print(files)

        write_result = await client.call_tool("write_to_file", {
            "filename": "test_mcp.txt", 
            "content": "Probando la herramienta de escritura."
        })
        print("\nResultado de escritura:")
        print(write_result)

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
