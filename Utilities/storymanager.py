import os
from .loader import load_json, save_json, process_directory

# Specify the path to the player's stats JSON file
player_stats_file = "player_stats.json"

# Specify the directory containing character JSON files
stories_directory = os.path.join(os.path.dirname(__file__), '..', 'Stories')

def check_stats() -> dict:
    """
    Load and return player stats from the JSON file.
    """
    player_stats = load_json(player_stats_file)
    return player_stats

def compare_stats(player_stats=None, characters_stats=None) -> str:
    """
    Compare player's stats with character stats and return available characters as a formatted string.

    Args:
        player_stats (dict): A dictionary containing the player's stats.
        characters_stats (dict): A dictionary containing character data.

    Returns:
        str: A formatted string containing character names that meet or exceed player's stats.
    """
    if not player_stats:
        player_stats = check_stats()
    if not characters_stats:
        characters_stats = process_directory()

    available_characters = []

    for character_name, character_data in characters_stats.items():
        character_stats = character_data.get(character_name, {}).get("stats", {})

        if (
            player_stats.get("jacked", 0) >= character_stats.get("jacked", 0) and
            player_stats.get("attraction", 0) >= character_stats.get("attraction", 0) and
            player_stats.get("looks", 0) >= character_stats.get("looks", 0)
        ):
            available_characters.append(character_name)

    if not available_characters:
        return "No one, get better rizz bro."

    formatted_characters = ', '.join(available_characters)
    return formatted_characters

def check_saves(character_name: str) -> str:
    character_story_data = load_json(os.path.join(stories_directory, f"{character_name}.json"))
    saved_at = character_story_data.get(character_name, {}).get("saved_at")
    return saved_at

def save_game(character_name: str, character_info: dict, current_story_index: int) -> None:
    character_info["saved_at"] = f"story{current_story_index}"
    character_story_data = load_json(os.path.join(stories_directory, f"{character_name}.json"))
    character_story_data[character_name] = character_info
    save_json(os.path.join(stories_directory, f"{character_name}.json"), character_story_data)
