from typing import Dict

from Utilities.interface import slow_print, clrscr
from Utilities.loader import load_json
from Player.Playerstats import update_player_stats

def load_clothes_json() -> Dict[str, int]:
    loaded_clothes_shop = load_json("./Activities/clothesShop.json")
    clothes_in_shop = loaded_clothes_shop.get("clothes", {})
    return clothes_in_shop

def clothes_shop() -> None:
    """Go shopping for clothes"""

    #loads json files
    player_stats = load_json("player_stats.json")

    slow_print("You walk into the shop and start picking out clothes.", sleepfor=1)

    while True: #This loop begins the shopping process
        clrscr()
        slow_print("Do you wish to shop? ", newlineend=False)
        will_buy = input().strip().lower() #asks player if they wish to shop (will_buy is meant to mean "will you buy something")

        if will_buy == "yes": #asks player if they wish to buy some clothes
            clrscr()
            for idx, (wear, price) in enumerate(load_clothes_json().items(), start = 1): #display shopping options to player
                slow_print(f"{wear} costs {price} - [{idx}]")
            slow_print("\nInput the name of the product you wish to buy: ", newlineend=False)
            buy_choice = input().strip().lower() #The buy_choice variable prompts the player

            if buy_choice in load_clothes_json(): #checks if the desired product is in the dict (this dict is inside clothesShop.json)
                clothes_price = load_clothes_json().get(buy_choice, 0) #gets the value of the item you bought
                update_player_stats(player_stats, clothes_price, looks='plus', money='minus') #updates plr stats, removing money and adding to looks
                slow_print(f"you bought {buy_choice} for ${clothes_price}.", sleepfor=1)

            else: #if the product is not in the dict, it reminds you so
                slow_print("Please enter a valid option!", sleepfor=1)

        else:
            slow_print("*You head home*", sleepfor=1) #sends player back to menu
            break
