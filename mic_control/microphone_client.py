from functools import partial
import subprocess


def execute_apple_script(command):
    result = subprocess.run(["osascript", "-e", command], stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    result = output.strip()
    return int(result)


SET_VOLUME_COMMAND = "set volume input volume {value}"
GET_INPUT_VOLUME_COMMAND = "input volume of (get volume settings)"
get_input_volume = partial(execute_apple_script, command=GET_INPUT_VOLUME_COMMAND)


class MacMicrophoneClient:
    def __init__(self):
        self.volume

    @property
    def volume(self):
        self._volume = get_input_volume()
        return self._volume

    @volume.setter
    def set_volume(self, value):
        if not (0 <= value <= 100):
            raise ValueError
        execute_apple_script(SET_VOLUME_COMMAND.format(value=value))
        self._volume = value

    def mute(self):
        self.volume = 0
