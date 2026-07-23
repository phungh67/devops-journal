import json, os
from pathlib import Path

root_dir = Path("/home/huyhoang/devops-journal/ai-ops")

def verify_template(file_name:str, module_name: str) -> dict:
    """Verification function, summary which was included in the template and what was missing
    
    Keyword arguments:
    file_name -- name of verification-needed file
    module_name -- name of module that contains this file, mostly prompts module
    """

    assertion_dict = {
        "null_value": 0,
        "total_keys": 0,
        "null_key": []
    }

    file_path = root_dir / module_name / file_name

    try:
        with open(file_path, "r") as file:
            template = json.load(file)
            for key in template.keys():
                if not template.get(key):
                    assertion_dict["null_value"] += 1
                    assertion_dict["null_key"].append(key)
                assertion_dict["total_keys"] += 1

    except FileNotFoundError:
        print(f"Error: The file at {file_path} does not exist or missed spelling?")
    
    return assertion_dict

if __name__ == "__main__":
    print("Test begin: ")
    res = verify_template("log_analyzer.json", "prompts/log_analyzer")

    print(json.dumps(res, indent=4))

    print("==================================================================\n")

    if res.get("null_key") == 0:
        print("RESULT: there are some null values in this file, verify it befor using...")
    else:
        print("RESULT: Passed")