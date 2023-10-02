import os
import json
from typing import Dict


directory_path = os.path.join(os.path.dirname(__file__), '..', 'stories')

def load_json(file_path: str) -> dict:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def save_json(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def process_directory(directory_path: str = directory_path) -> Dict[str, dict]:
    characters_stats = {}
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                character_name = os.path.splitext(file_name)[0]
                character_data = load_json(file_path)
                characters_stats[character_name] = character_data
    return characters_stats

def load_activities_module(module_name: str) -> ModuleType:
    module_spec = importlib.util.spec_from_file_location(
        module_name, f"./Activities/{module_name}.py"
    )
    activities_module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(activities_module)
    return activities_module
