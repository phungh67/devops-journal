import cmd
import json

from pydantic import ValidationError
from pathlib import Path

from classes.ollama_agent_connector import OllamaConnector
from classes.log import Triage
from prompts.log_analyzer.log_analyzer import log_analyzer

BASE_URL = "http://localhost:11434"
BASE_MODEL = "llama3.1"

class AgentDaemon(cmd.Cmd):
    prompt = "(agent) "

    def __init__(self):
        super().__init__()

        self.connector = OllamaConnector(BASE_URL, BASE_MODEL)
        self.active_triage: Triage | None = None

    def do_analyzer(self, arg):
        """Analyze a log file. Usage: analyze <filename>"""
        filename = arg if arg else "sample_log.txt"
        log_path = Path(__file__).parent / filename

        print(f"Analyzing {filename}...")

        raw_json_str = log_analyzer(self.connector, log_path)

        try:
            # Enforce the framework immediately
            parsed_dict = json.loads(raw_json_str)
            self.active_triage = Triage(**parsed_dict)
            print("\nAnalysis successful. Framework enforced.")
            print(self.active_triage.model_dump_json(indent=2))
        except ValidationError as e:
            print("[ERROR] LLM output failed framework enforcement:")
            print(e)
        except json.JSONDecodeError:
            print("[ERROR] Failed to decode raw LLM response.")

    def do_modify(self, arg):
        """Modify a root-level key. Usage: modify <key> <value>"""
        if not self.active_triage:
            print("No active state. Run 'analyze' first.")
            return

        args = arg.split(" ", 1)
        if len(args) < 2:
            print("Usage: modify <key> <new_value>")
            return

        key, new_val = args[0], args[1]
        
        # Dump current state to a dict
        current_data = self.active_triage.model_dump()
        
        if key not in current_data:
            print(f"[ERROR] '{key}' is not a valid field in the Triage framework.")
            return

        # Attempt the modification
        original_val = current_data[key]
        current_data[key] = new_val

        try:
            # Re-enforce the framework with the human modification
            self.active_triage = Triage(**current_data)
            print(f"Success: '{key}' updated.")
        except ValidationError as e:
            print(f"\n[REJECTED] Modification violates the framework constraints:\n{e}")
            # Revert is implicit since self.active_triage wasn't overwritten

    def do_show(self, arg):
        """Show the current valid state."""
        if self.active_triage:
            print(self.active_triage.model_dump_json(indent=2))
        else:
            print("No active triage data.")

    def do_exit(self, arg):
        return True

if __name__ == "__main__":
    AgentDaemon().cmdloop()  