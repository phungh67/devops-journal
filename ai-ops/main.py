from classes.ollama_agent_connector import OllamaConnector
from prompts.log_analyzer.log_analyzer import Triagle as tri_response

if __name__ == "__main__":
    new_connector = OllamaConnector()
    prompt = "How to theoretically update a thousands different images across a cluster with argoCD?"

    system_prompt = (
        "You are an expert DevOps engineer."
        "Should you only explain in 2 sentences."
    )

    new_connector.system_prompt = system_prompt

    resp = new_connector.generate_chat(tri_response, prompt)

    for key, val in resp.items():
        print(f"Key: {key}, Value: {val}")