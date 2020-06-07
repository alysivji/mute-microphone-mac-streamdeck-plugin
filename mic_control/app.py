#!/Users/alysivji/siv-dev/projects/home-automation/mute-microphone-mac-streamdeck-plugin/venv/bin/python

import argparse
import asyncio
import json
import logging

from pyee import AsyncIOEventEmitter
import websockets

from microphone_client import MacMicrophoneClient

logging.basicConfig(filename="example.log", level=logging.INFO)

microphone = MacMicrophoneClient()
ee = AsyncIOEventEmitter()


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
        await asyncio.sleep(60)
        microphone.volume


class StreamDeckClient:
    def __init__(self, port, event, plugin_uuid, info):
        logging.info(info)  # what's in here that we should save?
        self.plugin_uuid = plugin_uuid
        self.uri = f"ws://localhost:{port}"
        self.registration_info = {"event": event, "uuid": plugin_uuid}
        self.messages_to_send = []

    async def connect_and_listen(self):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(json.dumps(self.registration_info))
            await self.handle_messages(websocket)

    async def handle_messages(self, websocket):
        async for message in websocket:
            msg_dict = json.loads(message)
            logging.info(msg_dict)
            ee.emit(msg_dict["event"])


@ee.on('keyDown')
async def key_down_handler():
    microphone.toggle_mute()
    if microphone._volume == 0:
        # send state 1
        pass
    else:
        # send state 2
        pass


if __name__ == "__main__":
    logging.info("program started")
    args = parse_command_line_arguments()
    logging.info("parsed arguments")

    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(update_input_volume_from_system(), loop)
    streamdeck = StreamDeckClient(args.port, args.event, args.plugin_uuid, args.info)
    logging.info("here")
    loop.run_until_complete(streamdeck.connect_and_listen())

    logging.info("exited")
