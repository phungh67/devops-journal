import sys
import json

from pathlib import Path

from typing import Optional, Tuple

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent

sys.path.append(str(parent_dir))

from utils.verifier import verify_template
from utils.templater import template_loader

def hanlder_load_template_file(file_path: str, 
                               file_name: str, mode="r", 
                               base: Optional[str] = None) -> Tuple[Any, str]:
    try:
        if base is not None:
        # print(base)
            template_file = Path(f"{base}/{file_path}/{file_name}")
        else:
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

        print(json.dumps(template, indent=4))

    except FileNotFoundError as e:
        print(f"[ERROR] Cannot open file, maybe file is missing or not exist: {e}")

    return template, system_prompt

if __name__ == "__main__":
    root_dir = Path("/home/huyhoang/devops-journal/agentic")

    file_path = "prompts/log_analyzer"
    file_name = "log_analyzer.json"

    hanlder_load_template_file(file_path, file_name, "r", root_dir)