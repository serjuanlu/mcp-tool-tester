## Kata rápida

Haced un **fork** del repo y trabajad desde la rama `feature/langchain-agent` del tutorial MCP/LangChain. 

git switch feature/langchain-agent
git pull
git switch -c feature/new-mcp-tool


## Tarea
- Añadir una nueva tool en `servers/demo_server.py`.
- Hacer que `src/langchain_agent.py` la use.
- Crear otra rama para activar LangSmith y trazar la ejecución.

git switch feature/langchain-agent
git switch -c feature/langsmith-tracing

## LangSmith
LANGSMITH_API_KEY=tu_api_key_aqui
LANGSMITH_TRACING=TRUE
LANGSMITH_PROJECT=mcp-tool-tester

## Criterio de validación
- La tool funciona.
- El agente la usa.
- La traza aparece en LangSmith.