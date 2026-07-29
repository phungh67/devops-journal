from typing import Any, Optional

configuration_set = {}

def handle_set_configuration(mode: str, base: Optional[str] = None, path: Optional[str] = None) -> Any:
    if mode == "load":
        print("Loading a configuration file...")
        
