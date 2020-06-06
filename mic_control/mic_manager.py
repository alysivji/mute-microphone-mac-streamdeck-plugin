from functools import partial
import subprocess


def execute_apple_script(command):
    result = subprocess.run(["osascript", "-e", command], stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    result = output.strip()
    return int(result)


GET_INPUT_VOLUME_COMMAND = "input volume of (get volume settings)"
get_volume = partial(execute_apple_script, command=GET_INPUT_VOLUME_COMMAND)


def set_volume(value):
    if not (0 <= value <= 100):
        raise ValueError

    SET_VOLUME_COMMAND = f"set volume input volume {value}"
    execute_apple_script(SET_VOLUME_COMMAND)


mute_mic = partial(set_volume, value=0)
