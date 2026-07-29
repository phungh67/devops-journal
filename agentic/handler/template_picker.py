import sys

from pathlib import Path

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent

sys.path.append(str(parent_dir))

from utils.verifier import verify_template
from utils.templater import template_loader

def hanlder_load_template_file(file_path: str, file_name: str, mode="r"):
    try:
        otemplate, prompt = template_loader(file_path, file_name)

        print(otemplate)
        print(type(otemplate))

    except FileNotFoundError as e:
        print(f"[ERROR] Cannot open file, maybe file is missing or not exist: {e}")

if __name__ == "__main__":
    root_dir = Path("/home/huyhoang/devops-journal/ai-ops")

    file_path = "prompts/log_analyzer"
    file_name = "log_analyzer.json"

    hanlder_load_template_file(file_path, file_name)