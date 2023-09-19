import os
import json
from typing import Dict

def load_json(file_path: str) -> dict:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def save_json(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def check_stats(character_data: dict) -> dict:
    if "stats" in character_data:
        stats = character_data["stats"]
        # Perform operations with stats here
        print("Character Stats:", stats)
        return stats

def load_story(story_data: dict, story_name: str) -> None:
    print(f"Loading story from {story_name}:")
    for key, value in story_data.items():
        print(f"{key}: {value}")
    print("\n")

def load_stories(storizz_data: Dict[str, dict]) -> None:
    for story_name, story_data in storizz_data.items():
        load_story(story_data, story_name)

def process_directory(directory_path: str) -> Dict[str, dict]:
    characters_stats = {}
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                character_name = os.path.splitext(file_name)[0]
                character_data = load_json(file_path)
                characters_stats[character_name] = character_data
    return characters_stats

directory_path = os.path.join(os.path.dirname(__file__), '..', 'stories')  # Assuming 'utilities' and 'stories' are at the same level

"""def process_character_file(file_path):
    character_name = os.path.splitext(os.path.basename(file_path))[0]
    character_data = load_json(file_path)
    if character_name in character_data:
        character_data = character_data[character_name]
        check_stats(character_data)
        if "storizz" in character_data:
            storizz_data = character_data["storizz"]
            load_stories(storizz_data)
            return character_data
        else:
            print(f"No stories found for '{character_name}'.")
    else:
        print(f"Character '{character_name}' not found in the file.")"""