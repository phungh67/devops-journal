import requests
import json
import os
import time
from typing import Optional, Literal, Any
from pydantic import BaseModel

class Triage(BaseModel):
    """Class definition for the triagle response
    ---
    Contains 3 edges: Root_cause, confidence and next_step
    root_case: the very root theoretical cause of the phenomenol
    confidence: how reliable the response is
    next_step: what to do next
    """
    solution: str
    confidence: Literal["low", "medium", "high"]
    next_step: str


class OllamaConnector:
    """Class definition for Ollama connection
    ---
    This object create a session with on-going Ollama daemon.
    Normally, all properties was set to default values.
    Check the official documentations: https://docs.ollama.com/api/usage
    """

    def __init__(self, host: Optional[str]=None, model: Optional[str]=None,system_prompt: Optional[str]=None):
        """
        Constructor method for the object
        ---
        host: string - the endpoint to call Ollama, cloud or localhost, depends on the deployment
        model: string - currently supports one model at a time, pass the desired model here
        """
        self.host = host if host is not None else os.getenv("OLLAMA_HOST_URL", "http://localhost:11434")
        self.model = model if model is not None else os.getenv("OLLAMA_PREFER_MODEL", "gemma4")
        self.system_prompt = system_prompt if system_prompt is not None else ""

        # set the main group for api calling
        self.api_url = f"{self.host}/api/chat"

    def generate_chat(self, constraint: Triage, payload: str) -> dict:
        """Generate a chat and return a dictionary of response
        
        Keyword arguments:
        payload -- a string represents the input prompt1
        Return: a dictionary with response message, processing time, model name, input and output token
        """

        message = []
        if self.system_prompt != "": 
            # if there is any provided system prompt
            message.append({"role": "system", "content": self.system_prompt})
        message.append({"role": "user", "content": str(payload)})

        headers = {"Content-Type": "application/json"}

        formatted = constraint.model_json_schema()

        json_payload = {
            "model": self.model,
            "messages": message,
            "format": formatted,
            "stream": False
        }
        
        start = time.perf_counter()

        try:
            resp = requests.post(self.api_url, json=json_payload, headers=headers)
            resp.raise_for_status()

            resp = resp.json()

            resp = json.loads(resp['message']['content'])
            return resp
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request to OLLAMA failed with: {str(e)}.\n")
            return {"error": "request to Ollama failed"}

if __name__ == "__main__":
    new_connector = OllamaConnector()
    prompt = "How to update a thousands different images across a cluster with argoCD?"

    system_prompt = (
        "You are an expert DevOps engineer."
        "Should you only explain in 2 sentences."
    )

    new_connector.system_prompt = system_prompt

    resp = new_connector.generate_chat(prompt)

    for key, val in resp.items():
        print(f"Key: {key}, Value: {val}")
