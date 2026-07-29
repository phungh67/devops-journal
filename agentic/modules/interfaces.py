import sys
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from pathlib import Path

from typing import Optional

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent

sys.path.append(str(parent_dir))

from handler.handle_load_template import hanlder_load_template_file


def main():
    print("====================================")
    print("    WELCOME TO THE SYSTEM PORTAL    ")
    print("====================================\n")

    root_dir = Path("/home/huyhoang/devops-journal/agentic")

    file_path = "prompts/log_analyzer"
    file_name = "log_analyzer.json"
    
    while True:
        # Main menu keyboard-navigable dropdown
        action = inquirer.select(
            message="Select an action:",
            choices=[
                "View Profile",
                "Load a template",
                "Submit Bug Report",
                "Exit Application"
            ],
            default="View Profile",
        ).execute()

        if action == "View Profile":
            handle_view_profile()
        elif action == "Load a template":
            hanlder_load_template_file(file_path, file_name, "r", root_dir)
        elif action == "Submit Bug Report":
            handle_Submit_bug()
        elif action == "Exit Application":
            print("Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
