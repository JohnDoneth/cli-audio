import curses
import curses.textpad

import sys
from exceptions import CLIAudioScreenSizeError, CLIAudioFileError
from front.ListView import ListView, ListColumn, NavAction


class FrontEnd:
    """
    The frontend of the program using curses
    """
    def __init__(self, player):
        self.stdscr = curses.initscr()

        self.subwindow = None

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


    def display(self):
        """
        Draws the master window's text
        """
        self.stdscr.clear()

        self.stdscr.border()

        self.stdscr.addstr(1, 3, "cli-audio")
        self.stdscr.addstr(5, 5, "c - Change current song")
        self.stdscr.addstr(6, 5, "p - Play/Pause")
        self.stdscr.addstr(7, 5, "l - Library")
        self.stdscr.addstr(9, 5, "ESC - Quit")

        self.update_song()

        self.stdscr.touchwin()
        self.stdscr.refresh()

    def menu(self, args):
        """
        :param args:
        """

        self.display()

        try:
            while True:
                c = self.stdscr.getch()

                if c == curses.KEY_RESIZE:
                    y, x = self.stdscr.getmaxyx()
                    self.stdscr.clear()
                    curses.resize_term(x, y)
                    self.display()

                elif c == 27:
                    self.quit()

                elif c == ord('p'):
                    self.player.pause()

                elif c == ord('c'):
                    self.change_song()
                    self.update_song()

                elif c == ord('l'):
                    self.choose_from_library()

                self.display()

        except curses.error:
            raise CLIAudioScreenSizeError("Curses needs more space!")

    def update_song(self):
        """
        Update the GUI string that represents what song is playing
        """
        self.stdscr.addstr(15, 5, "                                        ")
        self.stdscr.addstr(15, 5, "Now playing: " + self.player.get_current_song())

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

    def library_song_selected(self, song):
        print(song)

    def choose_from_library(self):
        """
        Display the music library for the user
        """

        import glob
        import os

        filenames = ListColumn()
        filenames.header = "Filename"

        for file in glob.glob('./media/*.wav'):
            filenames.items.append(os.path.basename(file))



        columns = [filenames]

        #print(columns)

        list_view = ListView(self.stdscr, columns, self.library_song_selected)

        #list_view.display()

        self.subwindow = list_view
