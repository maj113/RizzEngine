from Utilities.interface import Mainmenu, slow_print, clrscr
from Player.Playerstats import view_or_modify_player_name

menu = Mainmenu()
clrscr()

if view_or_modify_player_name():

    slow_print(f"Welcome back {view_or_modify_player_name()}!", sleepfor=1)
else: menu.name_change()


menu.mainmenu()
