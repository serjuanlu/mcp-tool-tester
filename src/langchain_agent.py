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
            "content": "Eres un robot de archivos. SOLO usas herramientas. NO escribas explicaciones. Si te pido algo, usa la tool correspondiente inmediatamente."
        },
        {
            "role": "user",
            "content": "1. Usa list_files en '.', 'src' y 'servers'. 2. Usa read_project en 'servers/demo_server.py'. 3. Escribe un resumen de lo visto en el proyecto en 'RESUMEN.md' usando write_to_file. Saluda a Juanlu al final."
        }
    ]
    }
)

    for message in result["messages"]:
        print(message)


if __name__ == "__main__":
    asyncio.run(main())