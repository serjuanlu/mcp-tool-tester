# mcp-tool-tester
Template to connect to an MCP server and test tools
# para ollama
sudo apt update
sudo apt install -y zstd
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
# dejar en servicio y en otra pestaña del terminal
ollama pull qwen2.5:1.5b
python src/main.py

