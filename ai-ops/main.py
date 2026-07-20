from pathlib import Path

# class import
from classes.ollama_agent_connector import OllamaConnector

# prompt library import
# mostly function now
from prompts.log_analyzer.log_analyzer import log_analyzer

BASE_URL = "http://localhost:11434"
BASE_MODEL = "llama3.1"

if __name__ == "__main__":
    connector = OllamaConnector(BASE_URL, BASE_MODEL)

    log_dir = Path(__file__).parent
    log_path = log_dir / "sample_log.txt"

    resp = log_analyzer(connector, log_path)

    print(connector.efficiency)

    print(resp)