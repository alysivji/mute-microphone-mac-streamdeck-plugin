#!/Users/alysivji/siv-dev/playground/sandbox/javascript/streamdeck/venv/bin/python

import argparse
from functools import partial
import json
import logging
import os
import subprocess

import websocket

logging.basicConfig(filename="example.log", level=logging.DEBUG)


def execute_apple_script(command):
    result = subprocess.run(["osascript", "-e", command], stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    result = output.strip()
    return int(result)


GET_INPUT_VOLUME_COMMAND = "input volume of (get volume settings)"
input_volume = partial(execute_apple_script, command=GET_INPUT_VOLUME_COMMAND)


def set_volume(value):
    if not (0 <= value <= 100):
        raise ValueError

    SET_VOLUME_COMMAND = f"set volume input volume {value}"
    execute_apple_script(SET_VOLUME_COMMAND)


mute_mic = partial(set_volume, value=0)


def on_open(ws):
    logging.info(f"Input Volume {input_volume()}")
    # register device inside of program
    ws.send(json.dumps(registration_dict))
    # get settings


def on_message(ws, raw_message):
    items = json.loads(raw_message)
    if items["event"] == "keyUp":
        os.system('osascript -e "set volume input volume 0"')
    logging.info(raw_message)


def on_error(ws, error):
    logging.error(error)


def on_close(ws):
    logging.info("exited")


def parse_args():
    parser = argparse.ArgumentParser(description="StreamDeck Plugin")
    parser.add_argument("-port", dest="port")
    parser.add_argument("-pluginUUID", dest="plugin_uuid")
    parser.add_argument("-registerEvent", dest="event")
    parser.add_argument("-info", dest="info")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    registration_dict = {"event": args.event, "uuid": args.plugin_uuid}

    ws = websocket.WebSocketApp(
        "ws://localhost:" + args.port,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()
    logging.info("got all the way here")
