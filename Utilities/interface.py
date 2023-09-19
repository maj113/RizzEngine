import importlib.util
import os
from time import sleep
from random import uniform
from types import ModuleType

from .storymanager import compare_stats
from Player.Playerstats import display_player_stats


def load_activities_module(module_name) -> ModuleType:
    module_spec = importlib.util.spec_from_file_location(module_name, f"./Activities/{module_name}.py")
    activities_module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(activities_module)
    return activities_module

def get_first_docs_or_exec(module_name, execute: bool = False):
    # Load the activities module from the file
    activities_module = load_activities_module(module_name)
    
    callable_functions = []
    docstrings = []

    # Find callable functions and collect their docstrings
    for name, func in vars(activities_module).items():
        if callable(func):
            callable_functions.append(func)
            docstring = func.__doc__
            if docstring:
                docstrings.append(docstring.strip())

    if execute:
        clsscr()
        if callable_functions:
            # Execute the last callable function
            return callable_functions[-1]()

    # Return the docstring of the last callable function (or None if none found)
    if docstrings:
        return docstrings[-1]

    return None

def clsscr():
    """
    Clears the console screen using an escape sequence.
    """
    print("\033c", end="", flush=True)

def slow_print(text: str, speed: int = 5, sleepfor: int = 0, newlineend: bool = True, clear: bool = False):
    for char in text:
        print(char, end="", flush=True)
        sleep(uniform(0.1, 0.25) * (1 / speed))
    
    sleep(sleepfor)
    
    if newlineend:
        print()
    
    if clear:
        clsscr()


def check_activities():
    activities_path = "./Activities"
    activity_files = [f for f in os.listdir(activities_path) if f.endswith(".py")]
    
    if not activity_files:
        print("No activity files found in the 'Activities' folder.")
    else:
        clsscr()
        slow_print("Available Activities:\n", speed = 20)
        for idx, file_name in enumerate(activity_files, start=1):
            description = get_first_docs_or_exec(file_name[:-3])  # Remove '.py' extension
            if description:
                slow_print(f"   {description} [{idx}]")

        slow_print("\nSelect an activity (enter the number): ", newlineend=False)
        
        try:
            choice = int(input())
            if 1 <= choice <= len(activity_files):
                selected_module_name = activity_files[choice - 1][:-3]  # Remove '.py' extension
                get_first_docs_or_exec(selected_module_name, True)
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_stats():
    clsscr()
    display_player_stats()
    slow_print(f"\nYou can pick: {compare_stats()}", sleepfor=2, speed=10)


def available_options(selector: str = "main"):
    clsscr()
    if selector == "main":
        menu_options = [
            "Start new story [1]",
            "Continue Story [2]",
            "Do some activities [3]",
            "Check stats and characters [4]",
            "Save and Quit [5]\n"
        ]
        slow_print("\n".join(menu_options), speed=20)
    if selector == "activities":
        check_activities()



def mainmenu(choice: int = 0):
    while True:
        available_options()
        slow_print("what are you picking? ", newlineend=False)
        choice = int(input())
        if choice == 1:
            continue
        if choice == 2:
            continue
        if choice == 3:
            available_options(selector="activities")
        if choice == 4:
            display_stats()
        if choice == 5:
            clsscr()
            slow_print("Cya next time :)")
            break
        #else:
        #    clsscr()
        #    slow_print("Invalid option!", sleepfor=2)