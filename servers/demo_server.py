import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo MCP Server")

# --- HERRAMIENTAS DE LÓGICA Y PRUEBA ---

@mcp.tool()
def hello(name: str) -> str:
    """
    Saluda al usuario por su nombre. 
    Útil para verificar que la conexión básica funciona.
    """
    return f"Hola {name}, la tool MCP funciona bien."

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Suma dos números enteros y devuelve el resultado.
    """
    return a + b

# --- HERRAMIENTAS DE SISTEMA DE ARCHIVOS ---

@mcp.tool()
def list_files(directory: str = ".") -> str:
    """
    Lista todos los archivos y carpetas en el directorio especificado.
    Ayuda al agente a explorar la estructura del proyecto.
    """
    try:
        items = os.listdir(directory)
        if not items:
            return "El directorio está vacío."
        return "\n".join(items)
    except Exception as e:
        return f"ERROR al listar el directorio: {str(e)}"

@mcp.tool()
def read_project(filename: str) -> str:
    """
    Lee el contenido de un archivo específico dentro del proyecto.
    Devuelve los primeros 1000 caracteres para dar contexto a la IA.
    """
    try:
        # Construimos la ruta absoluta basada en el directorio de trabajo actual
        filepath = os.path.join(os.getcwd(), filename)

        if not os.path.exists(filepath):
            return f"ERROR: El archivo '{filename}' no existe."
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return content[:1000]
        
    except Exception as e:
        return f"ERROR al leer el archivo: {str(e)}"

@mcp.tool()
def write_to_file(filename: str, content: str) -> str:
    """
    Crea un archivo nuevo o sobreescribe uno existente con el contenido indicado.
    Restringido por seguridad a la carpeta raíz del proyecto.
    """
    try:
        if os.path.dirname(filename) and os.path.dirname(filename) != ".":
             return "ERROR: Por seguridad, solo puedes escribir archivos en la raíz del proyecto."
             
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Archivo '{filename}' guardado correctamente."
    except Exception as e:
        return f"ERROR al escribir el archivo: {str(e)}"

@mcp.tool()
def get_file_stats (filename: str) -> str:
    """
    Devuelve estadísticas básicas de un archivo, como tamaño y fecha de modificación.
    Ademas de cuenta de lineas, palabras y caracteres.
    Útil para que la IA evalúe la relevancia de un archivo antes de leerlo.
    """
    try:
        filepath = os.path.join(os.getcwd(), filename)
        if not os.path.exists(filepath):
            return f"ERROR: El archivo '{filename}' no existe."
        with open(filepath, 'r', encoding = 'utf-8')as f:
            content = f.read()
            lines = content.splitlines()
            words = content.split()
            chars = len(content)
            size = os.path.getsize(filepath)
            modified_time = os.path.getmtime(filepath)
        return (f"Estado del archivo '{filename}:\n"
                f"-Líneas: {len(lines)}\n"
                f"-Palabras: {len(words)}\n"
                f"-Caracteres: {chars}\n"
                f"-Tamaño: {size} bytes\n"
                f"-Última modificación: {modified_time}\n"
                )
    except Exception as e:
        return f"ERROR al obtener las estadísticas del archivo: {str(e)}"

# Ejecución del servidor
if __name__ == "__main__":
    mcp.run()