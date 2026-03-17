from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.session = None

    async def connect(self, command: str, args: list[str]):
        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=None,
        )

        transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        read_stream, write_stream = transport

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        await self.session.initialize()

    async def list_tools(self):
        result = await self.session.list_tools()
        return result.tools

    async def call_tool(self, tool_name: str, arguments: dict):
        return await self.session.call_tool(tool_name, arguments)

    async def close(self):
        await self.exit_stack.aclose()
