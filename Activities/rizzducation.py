from Utilities.interface import slow_print, display_stats, clrscr
from Utilities.loader import  load_json
from Player.Playerstats import update_player_stats
import random



def take_rizz_classes() -> None:
    """Take rizz classes from a trained professional (costs $30)"""
    
    # Load player stats
    player_stats = load_json("player_stats.json")

    #this is the money required to take one rizz class
    required_money = 30

    #random semi humorous qotes that appear while the player waits for the classes to end
    quotes = {
        1: " remembering the digits of pi",
        2: " scrolling phone cuz teacher boring",
        3: " quoting Napoleon",
        4: " thinking about girls",
        5: " actually listening",
        6: " billions must die",
        7: " I used to rule the world",
        8: " yassifying you"
    }

    # Get the desired workout time from the player
    while True:
        try:
            slow_print(
                "You decide to go take rizz classes tought by your school janitor. ", newlineend=False
            )
            clrscr()

            if required_money <= player_stats["money"]:
                break
            else:
                return slow_print("The janitor takes offense to your lackluster amount of money. BYE!", sleepfor=2)

        except ValueError:
            clrscr()
            slow_print("Input a number next time, jackass!", sleepfor=2, clear=True)


    # Display a workout animation
    for _ in range(5):
        slow_print(random.choice(quotes), sleepfor=8, newlineend=False)
    clrscr()

    # Update player stats
    update_player_stats(player_stats, 10, attraction='plus', money='minus')

    # Show post-workout message and updated stats
    slow_print(
        "By some miracle you managed to remember something.", sleepfor=2, newlineend=False
    )
    display_stats()

