import random

from Player.Playerstats import update_player_stats
from Utilities.interface import clrscr, display_stats, slow_print
from Utilities.loader import load_json
from Player.moneymanager import character_has_money

#this is the money required to take one rizz class
REQUIRED_MONEY = 30

#random semi humorous qotes that appear while the player waits for the classes to end
QUOTES = {
        1: " remembering the digits of pi",
        2: " scrolling phone cuz teacher boring",
        3: " quoting Napoleon",
        4: " thinking about girls",
        5: " actually listening",
        6: " billions must die",
        7: " I used to rule the world",
        8: " yassifying you"
    }

def activity_take_rizz_classes() -> None:
    """Take rizz classes from a trained professional (costs $30)"""

    # Load player stats
    player_stats = load_json("player_stats.json")

    slow_print(
        "You decide to go take rizz classes tought by your school janitor. ",
        newlineend=False, sleepfor=1
        )
    clrscr()
    #checks if player has enough money
    if character_has_money(REQUIRED_MONEY):

        # Display a taking notes animation
        for _ in range(5):
            slow_print(random.choice(list(QUOTES.values())), sleepfor=8, newlineend=False)
            clrscr()

        # Update player stats
        update_player_stats(player_stats, 10, attraction='plus', money='minus')

        # Show post-class message and updated stats
        slow_print(
            "By some miracle you managed to remember something.", sleepfor=2, newlineend=False
        )
        display_stats()

    else: slow_print(
        "The janitor takes offense to your lackluster amount of money. BYE!", sleepfor=2
    )
