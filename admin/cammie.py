import os
import sys
import time
from InquirerPy import inquirer
from loguru import logger

from config.config import ROOT_PATH, DB_PATH
from core.logging_decorator import log_execution


# === CORE MENU LOGIC === #

@log_execution
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

@log_execution
def back_to_main():
    print("\nReturning to main menu...\n")
    time.sleep(1)

@log_execution
def help_command():
    print("""
Cammie Help Menu
----------------
This is the central CLI tool for managing the Global Textile Arbitrage system.

Use this interface to initialize databases, run sourcing models, test, and manage reporting output.

Navigate by selecting options. Use ESC to back out of any submenu.
""")
    input("\nPress Enter to return...")

@log_execution
def exit_console():
    print("\nExiting Cammie CLI. Goodbye!\n")
    sys.exit(0)


# === CRUD STRUCTURE === #

def setup_menu():
    options = [
        "Initialize DB",
        "Seed Sample Data",
        "Add Product / Region / Source",
        "Back", "Help", "Exit"
    ]
    while True:
        choice = inquirer.select(message="🛠  Setup Menu", choices=options).execute()
        if choice == "Initialize DB":
            print("TODO: Call DB init function here")
        elif choice == "Seed Sample Data":
            print("TODO: Call seed function here")
        elif choice == "Add Product / Region / Source":
            print("TODO: Add entity logic")
        elif choice == "Help":
            help_command()
        elif choice == "Exit":
            exit_console()
        else:
            break


def read_menu():
    options = [
        "Run Pytest", "Generate Allure Report", "View Scoreboard", "Print DB State",
        "Back", "Help", "Exit"
    ]
    while True:
        choice = inquirer.select(message="📖  Read Menu", choices=options).execute()
        if choice == "Run Pytest":
            print("TODO: Run pytest command")
        elif choice == "Generate Allure Report":
            print("TODO: Generate Allure")
        elif choice == "View Scoreboard":
            print("TODO: Pull sourcing_scores")
        elif choice == "Print DB State":
            print(f"DB Path: {DB_PATH}")
        elif choice == "Help":
            help_command()
        elif choice == "Exit":
            exit_console()
        else:
            break


def update_menu():
    options = [
        "Add Tariff", "Update FX", "Refresh Data",
        "Back", "Help", "Exit"
    ]
    while True:
        choice = inquirer.select(message="🔁  Update Menu", choices=options).execute()
        if choice == "Add Tariff":
            print("TODO: Add new tariff")
        elif choice == "Update FX":
            print("TODO: Update currency rates")
        elif choice == "Refresh Data":
            print("TODO: Full refresh process")
        elif choice == "Help":
            help_command()
        elif choice == "Exit":
            exit_console()
        else:
            break


def delete_menu():
    options = [
        "Restore Clean DB", "Purge Logs", "Wipe Config Overrides",
        "Back", "Help", "Exit"
    ]
    while True:
        choice = inquirer.select(message="🔥  Delete Menu", choices=options).execute()
        if choice == "Restore Clean DB":
            confirm = inquirer.confirm(message="Are you sure? This will wipe all data.").execute()
            if confirm:
                print("TODO: Restore clean db logic")
        elif choice == "Purge Logs":
            print("TODO: Delete old logs")
        elif choice == "Wipe Config Overrides":
            print("TODO: Reset config values")
        elif choice == "Help":
            help_command()
        elif choice == "Exit":
            exit_console()
        else:
            break


# === ROOT MENU === #

@log_execution
def cammie_cli():
    while True:
        clear_console()
        options = [
            "1. Setup (Create)",
            "2. Read (Test & Report)",
            "3. Update (Modify)",
            "4. Delete (Restore)",
            "Help", "Exit"
        ]
        choice = inquirer.select(message="💬  Welcome to Cammie CLI", choices=options).execute()
        match choice:
            case "1. Setup (Create)":
                setup_menu()
            case "2. Read (Test & Report)":
                read_menu()
            case "3. Update (Modify)":
                update_menu()
            case "4. Delete (Restore)":
                delete_menu()
            case "Help":
                help_command()
            case "Exit":
                exit_console()

if __name__ == "__main__":
    cammie_cli()