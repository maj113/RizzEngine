import os
import sys
from time import sleep
from random import uniform
from typing import Any

from Player.Playerstats import display_player_stats, view_or_modify_player_name
from .storymanager import compare_stats, check_saves, save_game
from .loader import load_json,  load_activities_module, process_directory


def get_first_docs_or_exec(module_name: str, execute: bool = False) -> Any | None:
    # Load the activities module from the file
    activities_module = load_activities_module(module_name)

    # Find the first callable function with the "activity" prefix and collect its docstring
    for name, func in vars(activities_module).items():
        if callable(func) and name.startswith("activity"):
            docstring = func.__doc__
            if docstring:
                callable_function = func
                break  # Stop the loop when the first matching function is found

    if execute:
        clrscr()
        if callable_function:
            return callable_function()

    # Return the docstring of the first matching function (or None if none found)
    if docstring:
        return docstring.strip()

    return None

def clrscr() -> None:
    """
    Clears the console screen using the appropriate command based on the OS.
    """
    print("\033c", end="", flush=True)

def slow_print(
        text: str, speed: int = 5,
        sleepfor: int = 0, newlineend: bool = True,
        clear: bool = False
    ) -> None:
    for char in text:
        print(char, end="", flush=True)
        sleep(uniform(0.1, 0.25) * (1 / speed))

    sleep(sleepfor)

    if newlineend:
        print()

    if clear:
        clrscr()

#TODO: MOVE TO Storymanager.py
def start_story(character_name: str) -> None:
    character_story_data = load_json(f"./Stories/{character_name}.json")

    if character_name not in character_story_data:
        clrscr()
        slow_print(f"Character '{character_name}' not found in the Stories.")
        return

    character_info = character_story_data[character_name]

    if "intro" not in character_info:
        # Handle case where the character doesn't have an intro or has a broken story
        clrscr()
        slow_print(
            f"{character_name.capitalize()}"
            " doesn't have a valid story. Please pick another character.",
            sleepfor=2
        )
        return

    intro_text = character_info["intro"]
    clrscr()
    slow_print(intro_text)

    slow_print(f"Do you want to pick {character_name}? (yes/no): ", newlineend=False)
    choice = input().strip().lower()

    if choice != "yes":
        # Ask if they want to pick a different character
        clrscr()
        slow_print("Do you want to pick a different character? (yes/no): ", newlineend=False)
        choice = input().strip().lower()

        if choice == "yes":
            return  # Return to character selection
    clrscr()
    character_story = character_info.get("storizz", {})
    current_story_index = 0

    while f"story{current_story_index}" in character_story:
        story_segment = character_story[f"story{current_story_index}"]["story"]
        slow_print(f"{story_segment}\n", speed=8, sleepfor=2, clear=True)

        askout_count = 0

        for idx in range(1, 4):
            if f"askout{idx}" in character_story[f"story{current_story_index}"]:
                askout_count += 1
                choice_text = character_story[f'story{current_story_index}'][f'askout{idx}']
                line = f"  {choice_text} - [{idx}]"
                slow_print(line)

        if askout_count > 0:  # Check if there are askouts
            slow_print("\nWhich response are you picking? ", newlineend=False)

            choice = input().strip()
            clrscr()
            if choice == "menu":
                break  # Return to the main menu
            if choice.isdigit() and 1 <= int(choice) <= askout_count:
                choice_key = f"askout{choice}"
                reaction_key = f"reaction{choice}"
                if choice_key in character_story[f"story{current_story_index}"]:
                    reaction_text = character_story[f"story{current_story_index}"][reaction_key]
                    slow_print(f'{character_name.capitalize()}: {reaction_text}')
                else:
                    slow_print("No reaction text available for this choice.")
            else:
                slow_print("Invalid choice. Please enter a valid option.")

        # Save the game progress
        save_game(character_name ,character_info, current_story_index)

        current_story_index += 1

    else:
        # End of the story
        slow_print("End of the story.", sleepfor=2)

def check_activities() -> None:
    activities_path = "./Activities"
    activity_files = [
        f for f in os.listdir(activities_path) if f.endswith(".py") and f != "__init__.py"
    ]
    if not activity_files:
        print("No activity files found in the 'Activities' folder.")
    else:
        clrscr() 
        slow_print("Available Activities:\n", speed=20)
        idx = 1  # Initialize idx outside the loop
        for file_name in activity_files:
            description = get_first_docs_or_exec(file_name[:-3])  # Remove '.py' extension
            if description:
                slow_print(f"   {description} [{idx}]")
                idx += 1  # Increment idx only when description is truthy
        slow_print("\nSelect an activity (enter the number): ", newlineend=False)

        try:
            choice = int(input())
            if 1 <= choice <= len(activity_files):
                selected_module_name = activity_files[choice - 1][:-3]  # Remove '.py' extension
                get_first_docs_or_exec(selected_module_name, True)
            else:
                slow_print("Invalid choice. Please enter a valid number.", sleepfor=2)
        except ValueError:
            slow_print("Invalid input. Please enter a number.", sleepfor=2)


def character_selector() -> None:
    while True:
        clrscr()
        characters_stats = process_directory()
        formatted_characters = compare_stats()
        available_characters = []

        slow_print("Available Characters:\n")

        for idx, character_name in enumerate(characters_stats.keys(), start=1):
            formatted_name = f" {character_name.capitalize()} - [{idx}]"
            message = formatted_name

            if character_name not in formatted_characters:
                message += " - Cannot select"
            else:
                available_characters.append(character_name)

            # Check for save state
            if check_saves(character_name):
                message += " - In progress"

            slow_print(message)

        if not available_characters:
            slow_print(
                "You can't select any character, do some activities and increase your stats",
                sleepfor=2
            )
            return

        slow_print(
            "\nSelect a character (enter the number) or 'menu' to go back: ",
            newlineend=False
        )
        choice = input().strip()

        if choice == "menu":
            break
        if choice.isdigit() and 1 <= int(choice) <= len(characters_stats):
            selected_character_index = int(choice) - 1
            selected_character_name = list(characters_stats.keys())[selected_character_index]

            if selected_character_name in available_characters:
                # Check for save state
                if check_saves(character_name):
                    clrscr()
                    slow_print(
                        "You are about to overwrite the save state for"
                        f" {selected_character_name.capitalize()}. Continue? (yes/no): ",
                        newlineend=False
                    )
                    overwrite_choice = input().strip().lower()

                    if overwrite_choice == "yes":
                        start_story(selected_character_name)
                else:
                    start_story(selected_character_name)
            else:
                clrscr()
                slow_print(
                    "You can't select this character since your stats are too low",
                    sleepfor=2
                )
        else:
            clrscr()
            slow_print("Invalid choice. Please enter a valid option.", sleepfor=2)

def display_stats() -> None:
    clrscr()
    slow_print(display_player_stats(), newlineend=False)
    slow_print(f"\nYou can pick: {compare_stats()}", sleepfor=2, speed=10)

class Mainmenu:
    def __init__(self) -> None:
        self.menu_options = {
            "Start new story": self.start_new_story,
            "Continue Story": None,  # Placeholder for the continue action
            "Do some activities": self.activity_picker,
            "Check stats and characters": display_stats,
            "Change player's name": self.name_change,
            "Save and Quit": self.quit_game,
        }

        self.valid_choices = list(range(1, len(self.menu_options) + 1))

    def start_new_story(self) -> None:
        self.available_options("character_selection")

    def activity_picker(self) -> None:
        self.available_options("activities")

    def quit_game(self):
        clrscr()
        slow_print("Cya next time :)")
        sys.exit(0)

    def name_change(self):
        clrscr()
        name = input("What's your name? ")

        current_name = view_or_modify_player_name()
        if current_name is None:
            # No name is set, so we set the provided name
            view_or_modify_player_name(name)
            slow_print(f"Your name is now: {name}", sleepfor=2)
        elif current_name == name:
            # Don't change the name if it's the same
            clrscr()
            slow_print("Your name hasn't changed", sleepfor=2)
        else:
            # Ask for confirmation using slow_print
            clrscr()
            slow_print(
                f"Are you sure you want to update your name to '{name}'? (yes/no): ",
                newlineend=False
            )
            
            confirmation = input().strip().lower()
            clrscr()
            if confirmation == 'yes':
                ()
                view_or_modify_player_name(name)
                slow_print(f"Your name is now: {name}", sleepfor=2)
            else:
                slow_print("Name update cancelled.", sleepfor=2)
        

    def available_options(self, selector: str = "main") -> None:
        clrscr()
        if selector == "main":
            menu = [f"{menu_option} [{idx}]" for idx, menu_option in enumerate(
                    self.menu_options.keys(), start=1
                )
            ]
            slow_print("\n".join(menu), speed=20)
        if selector == "activities":
            check_activities()
        if selector == "character_selection":
            character_selector()

    def mainmenu(self) -> None:
        while True:
            self.available_options()
            slow_print("\nWhat are you picking? ", newlineend=False)
            choice = input()

            if not choice.isdigit():
                clrscr()
                slow_print("Invalid option!", sleepfor=2)
                continue

            choice = int(choice)
            if choice not in self.valid_choices:
                clrscr()
                slow_print("Invalid choice!", sleepfor=2)
                continue

            for idx, (_, function) in enumerate(self.menu_options.items(), start=1):
                if idx == choice and callable(function):
                    function()  # Call the associated function
                    break
