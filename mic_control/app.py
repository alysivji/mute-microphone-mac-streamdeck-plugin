#!/Users/alysivji/siv-dev/projects/home-automation/mute-microphone-mac-streamdeck-plugin/venv/bin/python

import argparse
import asyncio
import logging

from microphone_client import MacMicrophoneClient
from streamdeck_client import connect_and_listen

logging.basicConfig(filename="example.log", level=logging.INFO)

microphone = MacMicrophoneClient()


def parse_command_line_arguments():
    description = "Initalize StreamDeck plugin using command-line arguments"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-port", dest="port")
    parser.add_argument("-pluginUUID", dest="plugin_uuid")
    parser.add_argument("-registerEvent", dest="event")
    parser.add_argument("-info", dest="info")
    return parser.parse_args()


async def update_input_volume_from_system():
    while True:
        await asyncio.sleep(10)
        microphone.volume


if __name__ == "__main__":
    logging.info("program started")
    args = parse_command_line_arguments()
    logging.info("parsed arguments")
    registration_info = {"event": args.event, "uuid": args.plugin_uuid}
    logging.info(args.info)

    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(update_input_volume_from_system(), loop)
    loop.run_until_complete(connect_and_listen(registration_info, port=args.port))

    logging.info("exited")
