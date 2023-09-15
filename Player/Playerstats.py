import json
import random
import os

def generate_player_stats() -> dict[str, int]:
    player_stats = {
        "jacked": random.randint(20, 100),
        "attraction": random.randint(20, 100),
        "looks": random.randint(1, 5),
        "money": random.randrange(100, 1001, 50)
    }
    return player_stats

def save_player_stats_to_json(player_stats, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(player_stats, json_file, indent=4)

def load_player_stats_from_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    else:
        return None

def display_player_stats():
    player_stats = load_player_stats_from_json(json_file_path)

    if player_stats:
        from Utilities.interface import slow_print
        slow_print("Player Stats:\n")
        for stat, value in player_stats.items():
            slow_print(f"   {stat.capitalize()}: {value}")
    else:
        print("No player stats found.")

json_file_path = "player_stats.json"  # Change this to the desired file path

if not os.path.exists(json_file_path):
    player_stats = generate_player_stats()
    save_player_stats_to_json(player_stats, json_file_path)
