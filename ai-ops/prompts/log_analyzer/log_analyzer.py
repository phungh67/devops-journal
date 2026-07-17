import os
import json

from pathlib import Path
from typing import Optional, Literal, List

from pydantic import BaseModel

from classes.ollama_agent_connector import OllamaConnector

class Triage(BaseModel):
    """Definition, templating for the response from the AI agent
    
    Contains must have, must satisfy and must not be null fields.
    Should be used in collaboration with token count to measure the effective of prompts.
    """

    root_cause: str
    evidence: List[str]
    confidence: Literal["low", "medium", "high"]
    next_step: str

def log_analyzer(connector: OllamaConnector, log_text:str) -> dict:
    # currently only supported text log
    # @TODO: change to read log files or batch read
    """Reads JSON template for constraint, constructs the prompt and calls chat

    ---
    connector: an Ollama connector to be passed in this function
    log_text: a string of log to be fed as an evidence
    ---
    Return: a dictionary with structural as define via OllamaConnector (JSON)
    """

    template_path = Path(__file__).parent / "log_analyzer.json"

    with open(template_path, "r") as file:
        template = json.load(file)

    system_prompt = (
        f"Role: {template['Role']}\n"
        f"Context:  {json.dumps(template['Context'])}\n"
        f"Task: {template['Task']}\n"
        f"Rules: {' '.join(template['Expected'])}"
    )

    connector.system_prompt = system_prompt

    return connector.generate_chat(constraint=Triage, payload=log_text)