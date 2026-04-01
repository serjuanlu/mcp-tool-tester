import os
import asyncio
from dotenv import load_dotenv
load_dotenv()  
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama


async def main():
    client = MultiServerMCPClient(
        {
            "demo": {
                "transport": "stdio",
                "command": "python",
                "args": ["servers/demo_server.py"],
            }
        }
    )

    tools = await client.get_tools()

    model = ChatOllama(
        model="qwen2.5:1.5b",
        temperature=0,
    )

    agent = create_agent(model, tools)

    result = await agent.ainvoke(
    {
        "messages": [
            {
                "role": "system",
                "content": "Eres un analista de código. Usa 'list_files' para explorar y 'get_file_stats' para analizar archivos. Utiliza exclusivamente estas herramientas para interactuar con el sistema de archivos."            },
            {
                "role": "user",
                "content": "Busca un archivo con extensión '.md' en la carpeta actual y dime cuántas palabras tiene usando tu herramienta de estadísticas."            }
        ]
    }
)

    for message in result["messages"]:
        print(message)


if __name__ == "__main__":
    asyncio.run(main())