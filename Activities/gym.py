from Utilities.interface import slow_print, display_stats, clrscr
from Utilities.loader import  load_json
from Player.Playerstats import update_player_stats


def go_to_gym() -> None:
    """Go to the gym"""

    # Load player stats
    player_stats = load_json("player_stats.json")

    # Get the desired workout time from the player
    while True:
        try:
            slow_print(
                "You decide to go workout. How long do you wanna work out for? ", newlineend=False
            )
            workout_time = int(input())
            clrscr()

            if workout_time <= player_stats["money"]:
                break

            return slow_print("Brotha you broke asf, lazy ass mf go work", sleepfor=2)

        except ValueError:
            clrscr()
            slow_print("Input a number next time, jackass!", sleepfor=2, clear=True)


    # Display a workout animation
    for _ in range(workout_time):
        slow_print("💪", sleepfor=1, newlineend=False)
    clrscr()

    # Update player stats
    update_player_stats(player_stats, workout_time, jacked='plus', looks='plus', money='minus')

    # Show post-workout message and updated stats
    slow_print(
        "You feel better about yourself and you look a lot better.", sleepfor=2, newlineend=False
    )
    display_stats()
