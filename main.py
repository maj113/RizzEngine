from Utilities.interface import mainmenu, slow_print, clsscr
from Player.Playerstats import get_player_name

clsscr()

if get_player_name():

    slow_print("Welcome back!", sleepfor=1) 


mainmenu()
