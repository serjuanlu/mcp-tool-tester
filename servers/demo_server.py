from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo MCP Server")

@mcp.tool()
def hello(name: str) -> str:
    return f"Hola {name}, la tool MCP funciona bien."

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    mcp.run()
