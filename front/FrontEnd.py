import curses
import curses.textpad

import sys
from exceptions import CLIAudioScreenSizeError, CLIAudioFileError
from front.ListView import ListView, ListColumn

class FrontEnd:
    """
    The frontend of the program using curses
    """

    def __init__(self, player):
        self.stdscr = curses.initscr()

        # Try to use colors, but don't crash if we can't.
        try:
            curses.start_color()
            curses.use_default_colors()
        except curses.error:
            pass

        self.player = player

        if len(sys.argv) > 1:
            self.player.play(sys.argv[1])
            self.update_song()

        curses.wrapper(self.menu)

    def menu(self, args):
        """

        :param args:
        """
        try:
            self.stdscr.border()
            self.stdscr.addstr(0, 2, "cli-audio")
            self.stdscr.addstr(5, 10, "c - Change current song")
            self.stdscr.addstr(6, 10, "p - Play/Pause")
            self.stdscr.addstr(7, 10, "l - Library")
            self.stdscr.addstr(9, 10, "ESC - Quit")
            self.update_song()
            self.stdscr.refresh()
            while True:
                c = self.stdscr.getch()
                if c == 27:
                    self.quit()
                elif c == ord('p'):
                    self.player.pause()
                elif c == ord('c'):
                    self.change_song()
                    self.update_song()
                    self.stdscr.touchwin()
                    self.stdscr.refresh()
                elif c == ord('l'):
                    self.display_library()

        except curses.error:
            raise CLIAudioScreenSizeError("Curses needs more space!")

    def update_song(self):
        """
        Update the GUI string that represents what song is playing
        """
        self.stdscr.addstr(15, 10, "                                        ")
        self.stdscr.addstr(15, 10, "Now playing: " + self.player.get_current_song())

    def change_song(self):
        """
        Switch which song is playing
        """
        change_window = curses.newwin(5, 40, 5, 50)
        change_window.border()
        change_window.addstr(0, 0, "What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = change_window.getstr(1, 1, 30)
        curses.noecho()
        del change_window
        self.stdscr.touchwin()
        self.stdscr.refresh()
        self.player.stop()
        self.player.play(path.decode(encoding="utf-8"))

    def quit(self):
        """
        Exits the GUI and ends the program
        """
        self.player.stop()
        exit()

    def centered_window(self):
        """
        Creates a centered window
        """
        max_height, max_width = self.stdscr.getmaxyx()

        # height, width, begin_y, begin_x
        width = int(max_width / 2.0)
        height = int(max_height / 2.0)
        y = height / 2.0
        x = width / 2.0

        return curses.newwin(height, width, int(y), int(x))

    def display_library(self):
        """
        Display the music library for the user
        """

        import glob
        import os

        filenames = ListColumn()
        filenames.header = "Filename"

        for file in glob.glob('./media/*.wav'):
            filenames.items.append(os.path.basename(file))

        library_window = self.centered_window()
        library_window.border()
        library_window.addstr(0, 2, "Library")

        columns = [filenames]

        list_view = ListView(library_window, columns)

        library_window.refresh()

        self.stdscr.refresh()
