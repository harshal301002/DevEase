import json
import os
import sys

def load_config(config_path: str):
    if not os.path.isfile(config_path):
        print(f"[ERROR] Config file '{config_path}' not found.")
        sys.exit(1)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON from '{config_path}': {e}")
        sys.exit(1)
