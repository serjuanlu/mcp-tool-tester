import os
from langsmith import Client
from dotenv import load_dotenv
load_dotenv() 
# Verificamos si las variables están ahí
key = os.getenv("LANGSMITH_API_KEY")
print(f"¿API Key detectada?: {'SÍ' if key else 'NO'}")

client = Client()
try:
    # Intentamos una operación simple: listar proyectos
    projects = list(client.list_projects())
    print("✅ ¡Conexión exitosa! Proyectos encontrados:", [p.name for p in projects])
except Exception as e:
    print(f"❌ Error de conexión: {e}")