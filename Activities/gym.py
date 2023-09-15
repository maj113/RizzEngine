from Utilities.interface import slow_print
from Player.Playerstats import save_player_stats_to_json
import json


def go_to_gym():
    """Go to the jim brother"""
    slow_print("You decide to go workout. How long do you wanna work out for? ", newlineend=False)
    try:
        workoutTime = int(input())
    except ValueError:
        slow_print("Input a number next time, jackass!")
        return

    for time in range(workoutTime):
        
        slow_print("💪🏻", sleepfor=1, newlineend=False) 
    
    with open("player_stats.json", 'r') as json_file:
        player_stats = json.load(json_file)
    # Update the "jacked" stat
    player_stats["jacked"] += workoutTime
    player_stats["looks"] += workoutTime

    #Save the updated player stats back to the JSON file
    save_player_stats_to_json(player_stats, "player_stats.json")

    slow_print(f"\nYou feel better about yourself and you look a lot better.", sleepfor=3)