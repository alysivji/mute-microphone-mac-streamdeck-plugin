from functools import partial
import logging
import subprocess

logging.basicConfig(filename="example.log", level=logging.INFO)


def execute_apple_script(command):
    result = subprocess.run(["osascript", "-e", command], stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    result = output.strip()
    try:
        return int(result)
    except ValueError:
        return 0


SET_VOLUME_COMMAND = "set volume input volume {value}"
GET_INPUT_VOLUME_COMMAND = "input volume of (get volume settings)"
get_input_volume = partial(execute_apple_script, command=GET_INPUT_VOLUME_COMMAND)


class MacMicrophoneClient:
    def __init__(self, manager):
        self.manager = manager

    @property
    def volume(self):
        try:
            self._volume, self._previous_volume = get_input_volume(), self._volume
        except AttributeError:
            self._volume = get_input_volume()
            self._previous_volume = self._volume if self._volume != 0 else 70

        logging.info(f"previous {self._previous_volume}")
        logging.info(f"curr {self._volume}")
        return self._volume

    @volume.setter
    def volume(self, value):
        if not (0 <= value <= 100):
            raise ValueError
        execute_apple_script(SET_VOLUME_COMMAND.format(value=value))
        self._volume, self._previous_volume = value, self._volume

    def toggle_mute(self):
        if self._volume == 0:
            self.volume = self._previous_volume
        else:
            self.volume = 0
