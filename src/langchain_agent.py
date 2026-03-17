import asyncio

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
                "content": "Debes usar las herramientas disponibles para resolver la petición. No respondas de memoria si existe una tool adecuada."
            },
            {
                "role": "user",
                "content": "Llama obligatoriamente a la tool hello con name='Norbert' y después a la tool add con a=7 y b=5. Luego dame una frase final en español."
            }
        ]
    }
)

    for message in result["messages"]:
        print(message)


if __name__ == "__main__":
    asyncio.run(main())
