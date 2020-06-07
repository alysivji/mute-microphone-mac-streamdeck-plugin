#!/Users/alysivji/siv-dev/projects/home-automation/mute-microphone-mac-streamdeck-plugin/venv/bin/python

import argparse
import asyncio
import logging
from manager import MuteMicrophonePluginManager

logging.basicConfig(filename="example.log", level=logging.INFO)


def parse_command_line_arguments():
    description = "Initalize StreamDeck plugin using command-line arguments"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-port", dest="port")
    parser.add_argument("-pluginUUID", dest="plugin_uuid")
    parser.add_argument("-registerEvent", dest="event")
    parser.add_argument("-info", dest="info")
    return parser.parse_args()


logging.info("program started")
args = parse_command_line_arguments()


loop = asyncio.get_event_loop()
manager = MuteMicrophonePluginManager(args)
asyncio.run_coroutine_threadsafe(manager.update_input_volume_from_system(), loop)
loop.run_until_complete(manager.connect())

logging.info("exited")
