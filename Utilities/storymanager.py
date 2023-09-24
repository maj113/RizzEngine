import os
from typing import Dict
from .loader import load_json, process_directory

# Specify the path to the player's stats JSON file
player_stats_file = "player_stats.json"

# Specify the directory containing character JSON files
stories_directory = os.path.join(os.path.dirname(__file__), '..', 'Stories')

# Load player stats using the load_json function from loader.py
def check_stats() -> dict:
    player_stats = load_json(player_stats_file)
    return player_stats

# Use the process_directory function from loader.py to load character stats
def check_stories() -> Dict[str, dict]:
    characters_stats = process_directory(stories_directory)
    return characters_stats

# Use the process_directory function from loader.py to load character stats
def compare_stats(player_stats=None, characters_stats=None) -> str:
    """
    Compare player's stats with character stats and return available characters as a formatted string.

    Args:
        player_stats (dict): A dictionary containing the player's stats.
        characters_stats (dict): A dictionary containing character data.

    Returns:
        str: A formatted string containing character names that meet or exceed player's stats.
    """
    if player_stats is None:
        player_stats = check_stats()
    if characters_stats is None:
        characters_stats = check_stories()

    # Initialize an empty list to store available characters
    available_characters = []  

    # Iterate through the character data stored in the characters_stats dictionary
    for character_name, character_data in characters_stats.items():
        # Ensure you access the "stats" field within the character data correctly
        character_stats = character_data.get(character_name, {}).get("stats", {})

        # Check if the player's stats meet or exceed the character's stats
        if (
            player_stats["jacked"] >= character_stats.get("jacked", 0) and
            player_stats["attraction"] >= character_stats.get("attraction", 0) and
            player_stats["looks"] >= character_stats.get("looks", 0)
        ):  
            # Add the character to the available_characters list
            available_characters.append(character_name)  

    # Convert the list of character names into a formatted string
    if not available_characters:
        return "No one, get better rizz bro."
    formatted_characters = ', '.join(available_characters)

    return formatted_characters  # Return the formatted string

