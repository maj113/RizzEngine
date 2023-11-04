import os
import random
from typing import Dict

from Utilities.loader import load_json, save_json
test: Dict[str, Dict[str, int] | Dict[str, str] | Dict[str, Dict[str, str]]]
JSON_FILE_PATH = "player_stats.json"

def generate_player_stats() -> Dict[str, int | str]:
    created_player_stats = {
        "jacked": random.randint(20, 100),
        "attraction": random.randint(20, 100),
        "looks": random.randint(1, 5),
        "money": random.randrange(100, 1001, 50),
        "name" : ""
    }
    return created_player_stats

if not os.path.exists(JSON_FILE_PATH):
    saved_player_stats = generate_player_stats()
    save_json(JSON_FILE_PATH, saved_player_stats)

def display_player_stats() -> str:
    loaded_player_stats = load_json(JSON_FILE_PATH)
    stats_str = ""

    if loaded_player_stats:
        stats_str += "Player Stats:\n"
        for stat, value in loaded_player_stats.items():
            stats_str += f"   {stat.capitalize()}: {value}\n"

        return stats_str

    return "No player stats found."

def view_or_modify_player_name(name: str | None = None) -> str | None:
    stats = load_json(JSON_FILE_PATH)
    if not name and "name" not in stats:
        return None
    if not name:
        return stats["name"]
    update_player_stats(stats, name.capitalize(), name='change')

def update_player_stats(
        player_stats: Dict[str, str | int], stats_change: str | int, **stat_updates: str
    ) -> None:
    """
    Update player stats and save them to a JSON file.
    """
    # Update player stats based on the provided keyword arguments
    for stat_name, update_operator in stat_updates.items():
        if update_operator == 'plus':
            player_stats[stat_name] += stats_change
        elif update_operator == 'minus':
            player_stats[stat_name] -= stats_change
        elif update_operator == 'change':
            player_stats[stat_name] = stats_change
        # Add more cases for other update operators as needed

    # Save the updated player stats back to the JSON file
    save_json("player_stats.json", player_stats)
