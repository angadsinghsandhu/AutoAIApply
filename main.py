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
from io import StringIO

# local imports
# more db imports: get_row, add_row, update_row, delete_row, update_db_schema
from utils.notion.database import get_rows, get_db_schema

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

class StdoutRedirector:
    """
    Redirects stdout to write into the curses window with basic line-wrapping.
    """
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.buffer = StringIO()
        self.line = 0  # current line in the curses window

    def write(self, output):
        self.buffer.write(output)
        # If there's a newline in the output, flush immediately.
        # (This helps ensure prints appear in near real-time.)
        if '\n' in output:
            self.flush()

    def flush(self):
        # Move cursor to start of buffer
        self.buffer.seek(0)
        text = self.buffer.read()
        # Reset the buffer so future writes start fresh
        self.buffer = StringIO()

        # Split text into lines
        lines = text.split('\n')
        h, w = self.stdscr.getmaxyx()  # height, width of current window

        for line in lines:
            # Wrap each line if longer than the window width
            wrapped_chunks = [
                line[i : i + (w - 1)]  # w-1 to avoid a newline at last column
                for i in range(0, len(line), w - 1)
            ]
            # If the line is empty (just a newline), we want an empty chunk to move the cursor
            if not wrapped_chunks:
                wrapped_chunks = [""]

            for chunk in wrapped_chunks:
                # If we've run out of vertical space, wait for keypress and then clear screen
                if self.line >= h - 1:
                    self.stdscr.addstr(h - 1, 0, " -- More (press any key) --")
                    self.stdscr.refresh()
                    self.stdscr.getch()  # wait for user
                    self.stdscr.clear()
                    self.line = 0

                try:
                    self.stdscr.addstr(self.line, 0, chunk)
                except curses.error:
                    # If there's an error writing, we can safely ignore or handle differently
                    pass

                self.line += 1

        # Refresh screen to show newly printed lines
        self.stdscr.refresh()


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