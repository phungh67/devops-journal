import json

from pydantic import BaseModel

from verifier import verify_template

def template_loader(file_name: str) -> str:
    """Load a JSON template file and return a system prompt in string
    
    Keyword arguments:
    file_name(str) -- The name of template file, should be place inside prompts
    Return: a string representation for system prompt
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
    
    return system_prompt
