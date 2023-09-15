import importlib.util
import os
from time import sleep
from random import uniform

def load_activities_module(module_name):
    module_spec = importlib.util.spec_from_file_location(module_name, f"./Activities/{module_name}.py")
    activities_module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(activities_module)
    return activities_module

def get_first_docs_or_exec(module_name, execute: bool = False):
    activities_module = load_activities_module(module_name)
    
    for name, func in vars(activities_module).items():
        if callable(func):
            docstring = func.__doc__
            if docstring:
                if execute:
                    clsscr()
                    return func()
                first_line = docstring.strip().split('\n')[0]
                return first_line

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

def available_options(selector: str = "main"):
    if selector == "main":
        slow_print("Start new story [1]\n"
                    "Continue Story [2]\n"
                    "Do some activities [3]\n"
                    "Check stats and characters [4]\n"
                    "Save and Quit [5]\n", speed=25)
        return
    
    if selector == "activities":
        activities_path = "./Activities"
        activity_files = [f for f in os.listdir(activities_path) if f.endswith(".py")]
        
        if not activity_files:
            print("No activity files found in the 'Activities' folder.")
        else:
            clsscr()
            slow_print("Available Activities:", speed = 10)
            for idx, file_name in enumerate(activity_files, start=1):
                description = get_first_docs_or_exec(file_name[:-3])  # Remove '.py' extension
                if description:
                    slow_print(f"   {description} [{idx}]")
                    
            choice = input("Select an activity (enter the number): ")
            try:
                choice = int(choice)
                if 1 <= choice <= len(activity_files):
                    selected_module_name = activity_files[choice - 1][:-3]  # Remove '.py' extension
                    get_first_docs_or_exec(selected_module_name, True)
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")


def mainmenu(choice: int = 0):
    while True:
        clsscr()
        available_options()
        choice = int(input("what are you picking? "))
        if choice == 1:
            available_options()
        if choice == 2:
            available_options()
        if choice == 3:
            available_options(selector="activities")