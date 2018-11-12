"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time


class Player:
    """
    AudioPlayer
    """
    def __init__(self):
        # Instantiate PyAudio (1)
        self.p = pyaudio.PyAudio()

        self.currentSong = "N/A"
        self.paused = True
        self.position = 0
        self.stream = None
        self.wf = None

    def __del__(self):
        # Shutdown PyAudio
        self.p.terminate()

    def get_current_song(self):
        """
        Get what song is playing
        :return: The song that is playing
        """
        return self.currentSong

    def pause(self):
        """
        Pause the currently playing song
        """
        if self.stream is not None:
            if not self.paused:
                self.paused = True
                self.stream.stop_stream()
            else:
                self.paused = False
                self.stream.start_stream()

    def play(self, track):
        """
        Play the song
        :param track:
        """
        self.paused = False
        self.currentSong = track
        self.wf = wave.open(track, 'rb')

        # open self.stream using callback (3)
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  output=True,
                                  stream_callback=self.callback)

        # start the self.stream (4)
        self.stream.start_stream()

    def stop(self):
        """
        Stops the currently running music stream, if any.
        """
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()

        if self.wf is not None:
            self.wf.close()

    def callback(self, in_data, frame_count, time_info, status):
        """

        :param in_data:
        :param frame_count:
        :param time_info:
        :param status:
        :return:
        """
        data = self.wf.readframes(frame_count)
        return data, pyaudio.paContinue
