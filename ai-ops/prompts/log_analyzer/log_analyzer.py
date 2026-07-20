import os
import json

from pathlib import Path
from typing import Optional, Literal, List

from pydantic import BaseModel, Field

from classes.ollama_agent_connector import OllamaConnector

class Triage(BaseModel):
    """Definition, templating for the response from the AI agent
    
    Contains must have, must satisfy and must not be null fields.
    Should be used in collaboration with token count to measure the effective of prompts.
    """

    root_cause: str = Field(
        description="Exactly one sentence identifying the most likely root cause. If logs are insufficient, set to 'insufficient evidence' and list what is missing."
    )
    evidence: List[str] = Field(
        description="An array of log line snippets. Do not invent log lines. Quote them verbatim."
    )
    confidence: Literal["low", "medium", "high"] = Field(
        description="The confidence level of the root cause analysis."
    )
    next_step: str = Field(
        description="Exactly one concrete kubectl or curl command to execute next."
    )

def log_analyzer(connector: OllamaConnector, log_path:str) -> dict:
    # currently only supported text log
    # @TODO: change to read log files or batch read
    """Reads JSON template for constraint, constructs the prompt and calls chat

    ---
    connector: an Ollama connector to be passed in this function
    log_text: a string of log to be fed as an evidence
    ---
    Return: a dictionary with structural as define via OllamaConnector (JSON)
    """

    template_dir = Path(__file__).parent
    template_file = template_dir / "log_analyzer.json"

    with open(template_file, "r") as file:
        template = json.load(file)

    system_prompt = (
        f"Role: {template['Role']}\n"
        f"Context: {json.dumps(template['Context'])}\n"
        f"Task: {template['Task']}\n"
        f"Rules: {' '.join(template['Expected'])}\n"
        f"Constraint: {template['Output']['Constraint']}"
    )

    connector.system_prompt = system_prompt

    with open(log_path, "r") as file:
        file_content = file.read()

    return connector.generate_chat(constraint=Triage, payload=file_content)