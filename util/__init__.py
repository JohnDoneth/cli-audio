
import curses

def new_centered_window(parent):
    """
    Creates a centered window
    """
    parent_height, parent_width = parent.getmaxyx()

    # height, width, begin_y, begin_x
    width = int(parent_width / 2.0)
    height = int(parent_height / 2.0)
    y = height / 2.0
    x = width / 2.0

    return curses.newwin(height, width, int(y), int(x))