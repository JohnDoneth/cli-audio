# The PEP8 Python style guide, makes an explicit mention that
# “you should use the suffix ‘Error’ on your exception names
# ...so that's what I did!


class CLIAudioException(Exception):
    """Base class for other CLI-Audio exceptions"""

    def __init__(self, message):
        super().__init__(message)


class CLIAudioFileError(CLIAudioException):
    """An audio file was unable to be played"""

    def __init__(self, message):
        super().__init__(message)


class CLIAudioScreenSizeError(CLIAudioException):
    """An invalid screen size was requested"""

    def __init__(self, message):
        super().__init__(message)
