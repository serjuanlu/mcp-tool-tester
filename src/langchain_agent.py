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
        base_url="http://host.docker.internal:11434"
    )

    agent = create_agent(model, tools)

    result = await agent.ainvoke(
    {
        "messages": [
        {
            "role": "system",
            "content": """Eres un asistente que utiliza las tools para las tareas. 
            REGLA CRITICA: Si una tarea depende de otra, hazlas en orden y espera el resultado de la primera antes de ejecutar la segunda.
            Sigue estrictamente este protocolo:
            1.Analiza la pregunta del usuario y decide qué tools usar.
            2.No mezcles argumentos de diferentes tools, haz una llamada a la vez.
            3.Ejecuta las tools en orden logico para resolver la pregunta, si una tool depende de otra, espera su resultado.
            4.Si una tool retorna un error, pasa a la siguiente sin detener el proceso.
            5.Responde de forma concisa y no uses memoria si no es necesario. 
            6.Si el usuario hace una pregunta que no se puede resolver con las tools, responde que no puedes ayudar con esa pregunta."""
        },
        {
            "role": "user",
            "content": """
            1.Busca las coordenadas del punto central de 'Jodar, España' usando la tool creada. Espera la respuesta antes de continuar.
            2.Utiliza las coordenadas obtenidas para ejecutar la tool de clima get_weather y obtener el clima actual de las coordenadas dadas. Espera la respuesta antes de continuar.
            3.Crea un archivo con los datos obtenidos llamado 'RESUMEN{ciudad}.md' usando la tool write_to_file. 
            """
        }
    ]
    }
)

    for message in result["messages"]:
        print(message)

if __name__ == "__main__":
    asyncio.run(main())