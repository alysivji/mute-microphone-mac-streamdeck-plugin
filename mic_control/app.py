#!/Users/alysivji/siv-dev/projects/home-automation/mute-microphone-mac-streamdeck-plugin/venv/bin/python

import argparse
import asyncio
import json
import logging

import websockets

logging.basicConfig(filename="example.log", level=logging.INFO)


async def handle_messages(websocket):
    async for message in websocket:
        msg_dict = json.loads(message)
        logging.info(msg_dict)
        # if msg_dict["event"] == "keyUp":
        #     os.system('osascript -e "set volume input volume 0"')


async def connect_and_listen(registration_info: dict, port: int):
    uri = f"ws://localhost:{port}"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(registration_info))
        await handle_messages(websocket)


def parse_args():
    parser = argparse.ArgumentParser(description="StreamDeck Plugin")
    parser.add_argument("-port", dest="port")
    parser.add_argument("-pluginUUID", dest="plugin_uuid")
    parser.add_argument("-registerEvent", dest="event")
    parser.add_argument("-info", dest="info")
    return parser.parse_args()


if __name__ == "__main__":
    logging.info("program started")
    args = parse_args()
    logging.info("parsed arguments")
    registration_info = {"event": args.event, "uuid": args.plugin_uuid}
    logging.info(args.info)
    loop = asyncio.get_event_loop()
    # schedule function to periodically get value from macbook
    loop.run_until_complete(connect_and_listen(registration_info, port=args.port))
    loop.run_forever()
    logging.info("exited")
