"""
Columns to be displayed in a ListView
"""

import curses.panel
from _curses import A_REVERSE, A_BLINK
from enum import Enum


class NavAction(Enum):
    Up = 1
    Down = 2
    Select = 3
    Escape = 4


class ListColumn:
    header = ""
    items = []


class ListView:
    """
    Displays a list with detail columns
    """

    window = None

    def __init__(self, window, columns, select_callback):

        self.index = 0
        self.window = window
        self.columns = columns
        self.select_callback = select_callback
        self.display()

    def display(self):
        # Hide cursor
        curses.curs_set(0)

        curses.panel.new_panel(self.window)

        max_height, max_width = self.window.getmaxyx()

        column_width = int((max_width - 1) / len(self.columns))

        for i, column in enumerate(self.columns):
            self.window.addstr(1 + i, 1, column.header)

            # Display each item
            for j, item in enumerate(column.items):

                if self.index == j:
                    # add str @ y, x
                    self.window.addstr(2 + j, 1 + (i * column_width), item, A_REVERSE)
                else:
                    # add str @ y, x
                    self.window.addstr(2 + j, 1 + (i * column_width), item)

        self.window.refresh()

    def navigate(self, action):

        if action == NavAction.Down:
            self.index = self.index + 1

        elif action == NavAction.Up:
            self.index = self.index - 1

        elif action == NavAction.Select:
            print("selected")
            # construct the row list to pass to the function
            row = []
            for column in self.columns:
                row.append(column.items[self.index])

            # pass the row list to the function
            self.select_callback(row)

        self.calc_index_bounds()
        self.display()
        self.window.refresh()

    def calc_index_bounds(self):
        if self.index < 0:
            self.index = 0

        if len(self.columns) > 0:
            if self.index > len(self.columns[0].items) - 1:
                self.index = len(self.columns[0].items) - 1
