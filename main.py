"""
FILE: main.py

DESCRIPTION: This file is the main entry point for the application. 
It is responsible for initializing the application, parsing command-line
arguments, and calling core functions.
"""
# global imports
import os
import sys
import json
import curses
import argparse
from dotenv import load_dotenv

# local imports
# more db imports: get_row, add_row, update_row, delete_row, update_db_schema
from src.notion.database import get_rows, get_db_schema
from src.utils.redirector import StdoutRedirector

# Load environment variables from .env file
load_dotenv()

# Notion API Configuration
NOTION_API_URL = os.getenv("NOTION_API_URL")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = "1674d51105a8805f8312e91518420596"

# Notion API Headers
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"  # Ensure compatibility with the API version
}


# TODO: parse the correct args
def parse_args():
    """
    Parse command-line arguments and return them as an object.
    """
    parser = argparse.ArgumentParser(description="A simple image viewer application.")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")

    # additional arguments

    return parser.parse_args()


def test(stdscr):
    """
    Test the Notion API and display results in the curses window.
    """
    redirector = StdoutRedirector(stdscr)
    original_stdout = sys.stdout

    # Redirect all prints to the curses window
    sys.stdout = redirector

    # ---- START TEST LOGIC ----
    print("Getting all rows from the database...")
    rows = get_rows(DATABASE_ID, HEADERS)
    print(json.dumps(rows, indent=2))

    print("\nGetting the database schema...")
    schema = get_db_schema(DATABASE_ID, HEADERS)
    print(json.dumps(schema, indent=2))
    # ---- END TEST LOGIC ----

    # Make sure everything is flushed out
    redirector.flush()

    # Restore original stdout
    sys.stdout = original_stdout


def main(stdscr):
    """
    Main entry function for the application.
    """
    # Clear screen
    stdscr.clear()

    # Menu options
    menu = [
        'Run Test Function',
        'Check Email',
        'Get New Jobs',
        'Fill Job Info',
        'Exit'
    ]
    current_row = 0

    def print_menu(selected_row_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        for idx, row in enumerate(menu):
            x = w // 2 - len(row) // 2
            # place the menu roughly in the vertical center
            y = h // 2 - len(menu) // 2 + idx
            if idx == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
        stdscr.refresh()

    # Initialize curses settings
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    print_menu(current_row)

    while True:
        key = stdscr.getch()

        # Navigate up/down
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        # Enter key pressed
        elif key in [curses.KEY_ENTER, 10, 13]:
            # Option 0 -> Run Test Function
            if current_row == 0:
                stdscr.clear()
                stdscr.addstr(0, 0, "Running test function...\n\n")
                stdscr.refresh()

                # Run the test and display everything
                test(stdscr)

                # Once test is done, ask user to press a key
                stdscr.addstr("\nPress any key to return to the menu.")
                stdscr.refresh()
                stdscr.getch()

                # Clear screen & reprint menu
                print_menu(current_row)

            # Option 1 -> Check Email
            # Option 2 -> Get New Jobs
            # Option 3 -> Fill Job Info
            elif current_row in [1, 2, 3]:
                stdscr.clear()
                stdscr.addstr(0, 0, "This option is not implemented yet.\n")
                stdscr.addstr("\nPress any key to return to the menu.")
                stdscr.refresh()
                stdscr.getch()
                print_menu(current_row)

            # Option 4 -> Exit
            elif current_row == 4:
                break

        print_menu(current_row)

if __name__ == "__main__":
    args = parse_args()
    curses.wrapper(main)