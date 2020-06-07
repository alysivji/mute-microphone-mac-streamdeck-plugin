class FakeMicrophoneClient():
    def __init__(self, volume=None, previous_volume=None):
        if volume:
            self._volume = volume
        if previous_volume:
            self._previous_volume = previous_volume
