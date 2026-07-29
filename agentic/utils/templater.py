import json

from pathlib import Path
from typing import Tuple, Any
from pydantic import BaseModel

def template_loader(file_path: str, file_name: str) -> Tuple[Any, str]:
    """Load a JSON template file and return a system prompt in string
    
    Keyword arguments:
    file_name(str) -- The name of template file, should be place inside prompts
    Return: a string representation for system prompt
    """

    template_file = Path(f"{file_path}/{file_name}")

    with open(template_file, "r") as file:
        template = json.load(file)

    
    
    system_prompt = (
        f"Role: {template['Role']}\n"
        f"Context: {json.dumps(template['Context'])}\n"
        f"Task: {template['Task']}\n"
        f"Rules: {' '.join(template['Expected'])}\n"
        f"Constraint: {template['Output']['Constraint']}"
    )
    
    return template, system_prompt
