import random
import os
from typing import Any, Dict

from Utilities.loader import load_json, save_json

json_file_path = "player_stats.json"  # Change this to the desired file path

def generate_player_stats() -> Dict[str, int]:
    player_stats = {
        "jacked": random.randint(20, 100),
        "attraction": random.randint(20, 100),
        "looks": random.randint(1, 5),
        "money": random.randrange(100, 1001, 50)
    }
    return player_stats

if not os.path.exists(json_file_path):
    player_stats = generate_player_stats()
    save_json(json_file_path, player_stats)

def display_player_stats() -> None:
    player_stats = load_json(json_file_path)

    if player_stats:
        from Utilities.interface import slow_print
        slow_print("Player Stats:\n")
        for stat, value in player_stats.items():
            slow_print(f"   {stat.capitalize()}: {value}")
    else:
        print("No player stats found.")

def get_player_name() -> str:
    stats = load_json(json_file_path)
    name = str(stats.get("name"))
    if not name:
        create_player_name(stats)
    return name

def create_player_name(stats: dict) -> str:
    from Utilities.interface import slow_print
    slow_print("What's your name? ", newlineend=False)
    new_name = str(input()).capitalize()
    update_player_stats(stats, new_name, name='change')
    return new_name

def update_player_stats(
        player_stats: Dict[str, int], stats_change: Any, **stat_updates: str
    ) -> None:
    """
    Update player stats and save them to a JSON file.

    Args:
        player_stats (dict): A dictionary containing player statistics.
        stats_change (int): The amount by which the stats should be updated.
        **stat_updates: Keyword arguments specifying the update operator for each stat.
            Use 'plus' for addition and 'minus' for subtraction.

    Example:
        To update 'jacked' and 'looks' with addition and 'money' with subtraction:
        update_and_save_player_stats(player_stats, 10, jacked='plus', looks='plus', money='minus')
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