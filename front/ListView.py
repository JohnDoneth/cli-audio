"""
Columns to be displayed in a ListView
"""

import curses.panel
from _curses import A_REVERSE, A_BLINK
from enum import Enum

class NavAction(Enum):
    Up     = 1
    Down   = 2
    Select = 3
    Escape = 4


class ListColumn:
    header = ""
    items = []

class ListView:
    """
    Displays a list with detail columns
    """
    def __init__(self, window, columns):

        self.index = 0
        self.window = window

        # Hide cursor
        curses.curs_set(0)

        curses.panel.new_panel(self.window)

        max_height, max_width = self.window.getmaxyx()

        column_width = int((max_width - 1) / len(columns))

        for i, column in enumerate(columns):
            self.window.addstr(1 + i, 1, column.header)

            # Display each item
            for j, item in enumerate(column.items):


                if self.index == j:
                    # add str @ y, x
                    self.window.addstr(2 + j, 1 + (i * column_width), item, A_REVERSE)
                else:
                    # add str @ y, x
                    self.window.addstr(2 + j, 1 + (i * column_width), item)

        self.navigate()

    def navigate(self):
        while True:
            c = self.window.getch()

            if c == ord('q'):
                self.index = self.index + 1
            else:
                self.index = self.index - 1

        pass
