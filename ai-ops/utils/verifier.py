import json
from pathlib import Path

def verify_template(file_path:str) -> dict:
    """Verification function, summary which was included in the template and what was missing
    
    Keyword arguments:
    argument -- path leads to the file, using relative path in this case
    """

    assertion_dict = {
        "null_value": 0,
        "total_keys": 0,
        "null_key": []
    }

    with open(file_path, "r") as file:
        template = json.load(file)
    
    for key in template.keys():
        if not template.get(key):
            assertion_dict["null_value"] += 1
            assertion_dict["null_key"].append(key)
        assertion_dict["total_keys"] += 1
    
    return assertion_dict

if __name__ == "__main__":
    print("Test begin: ")
    res = verify_template("test.json")

    print(json.dumps(res, indent=4))