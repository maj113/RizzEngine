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

json_file_path = "player_stats.json"  # Change this to the desired file path

if not os.path.exists(json_file_path):
    player_stats = generate_player_stats()
    save_player_stats_to_json(player_stats, json_file_path)
