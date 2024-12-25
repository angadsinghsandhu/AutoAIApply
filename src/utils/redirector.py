'''
File: redirector.py

Description: Utility functions for redirecting stdout to a curses window.
'''

# local imports
import curses
from io import StringIO

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