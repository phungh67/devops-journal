import os
import json
from pathlib import Path
from typing import Optional

from classes.ollama_agent_connector import OllamaConnector
from classes.terraform import TerraformReview

def tf_reviewer(connector: OllamaConnector, tf_path: str, context_override: dict = None) -> dict:
    """Reads JSON template for constraint, constructs the prompt and calls chat

    ---
    connector: an Ollama connector to be passed in this function
    tf_path: a string path of the terraform file to be fed as evidence
    context_override: a dictionary to temporarily override context values
    ---
    Return: a dictionary with structural as define via OllamaConnector (JSON)
    """

    template_dir = Path(__file__).parent
    template_file = template_dir / "tf_reviewer.json"

    with open(template_file, "r") as file:
        template = json.load(file)

    # Apply context overrides dynamically
    current_context = template['Context']
    if context_override:
        current_context.update(context_override)

    # Assemble the system prompt with Format Requirements
    system_prompt = (
        f"Role: {template['Role']}\n"
        f"Context: {json.dumps(current_context)}\n"
        f"Task: {template['Task']}\n"
        f"Rules: {' '.join(template['Expected'])}\n"
        f"Constraint: {template['Output']['Constraint']}\n"
        f"Format Requirements: {json.dumps(template['Output']['Format'])}"
    )

    connector.system_prompt = system_prompt

    # Read the Terraform file and inject line numbers for the LLM
    with open(tf_path, "r") as file:
        raw_content = file.readlines()
    
    numbered_content = "".join([f"{i+1:03d} | {line}" for i, line in enumerate(raw_content)])

    # Generate chat using the TerraformReview schema
    return connector.generate_chat(constraint=TerraformReview, payload=numbered_content)