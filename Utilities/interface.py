
from time import sleep
from random import uniform

def clsscr():
    """
    Clears the console screen using an escape sequence.
    """
    print("\033c", end="", flush=True)

def slow_print(text, speed = 5):
    for char in text:
        print(char, end="", flush = True)
        sleep(uniform(0.1,0.25)*(1/speed))
