from Utilities.interface import mainmenu, slow_print, clrscr
from Player.Playerstats import get_player_name

clrscr()

if get_player_name():

    slow_print(f"Welcome back {get_player_name()}!", sleepfor=1) 


mainmenu()