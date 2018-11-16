"""
ListView object that displays a list of columns and runs a callback on a selection
"""

import curses.panel
from _curses import A_REVERSE, A_BLINK
from enum import Enum

import util


class NavAction(Enum):
    """
    The navigation actions that can be applied to a ListView
    """
    Up = 1
    Down = 2
    Select = 3
    Escape = 4


class ListColumn:
    """
    The columns passed to the ListView constructor to apply
    """
    header = ""
    items = []


class ListView:
    """
    Displays a list with detail columns
    """
    window = None

    def __del__(self):
        del self.window

    def __init__(self, parent, columns, select_callback):

        self.parent = parent

        self.window = util.new_centered_window(parent)
        self.window.border()
        self.window.addstr(0, 2, "Library")

        self.index = 0
        self.columns = columns
        self.select_callback = select_callback

        curses.panel.new_panel(self.window)

        # Allow curses to translate some keys in enum keys
        self.window.keypad(True)

        self.display()

        while True:
            c = self.window.getch()

            if c == curses.KEY_UP:
                self.navigate(NavAction.Up)

            elif c == curses.KEY_DOWN:
                self.navigate(NavAction.Down)

            elif c == curses.KEY_RESIZE:
                #y, x = self.parent.getmaxyx()
                #self.parent.clear()
                #curses.resize_term(x, y)
                self.display()

            # The ASCII value for '\n'. Do not use curses.KEY_ENTER as that is the num-pad enter key
            elif c == 10:
                self.navigate(NavAction.Select)

            elif c == 27:
                break

            self.display()

    def display(self):
        """
        Displays the column's header and contents
        """
        # Hide cursor
        curses.curs_set(0)

        self.window.clear()
        self.window.border()

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

        self.window.touchwin()
        self.window.refresh()

    def navigate(self, action):
        """
        Accepts an action to apply to the current ListView state
        :param action: The action to execute
        """
        if action == NavAction.Down:
            self.index = self.index + 1

        elif action == NavAction.Up:
            self.index = self.index - 1

        elif action == NavAction.Select:
            print("selected")
            # construct the row list to pass to the function
            #row = []
            #for column in self.columns:
            #    row.append(column.items[self.index])

            # pass the selected song to the callback function
            self.select_callback(self.columns[0].items[self.index])

        self.calc_index_bounds()
        self.display()

        print("navigated")

    def calc_index_bounds(self):
        """
        Utility method to make sure the cursor stays within the bounds of the list
        """
        if self.index < 0:
            self.index = 0

        if len(self.columns) > 0:
            if self.index > len(self.columns[0].items) - 1:
                self.index = len(self.columns[0].items) - 1
