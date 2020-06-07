import json
import logging
from typing import NamedTuple

from pyee import AsyncIOEventEmitter
import websockets


ee = AsyncIOEventEmitter()


class Device(NamedTuple):
    id: str
    name: str


class StreamDeckClient:
    def __init__(self, port, event, plugin_uuid, info, mic):
        self.devices = {d["id"]: Device(d["id"], d["name"]) for d in info["devices"]}
        self.plugin_uuid = plugin_uuid
        self.uri = f"ws://localhost:{port}"
        self.registration_info = {"event": event, "uuid": plugin_uuid}
        self.message_queue = []
        self.mic = mic
        import pdb; pdb.set_trace()
        logging.info(self.devices)

    async def connect_and_listen(self):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(json.dumps(self.registration_info))
            await self.handle_messages(websocket)

    async def handle_messages(self, websocket):
        async for message in websocket:
            msg_dict = json.loads(message)
            logging.info(msg_dict)
            ee.emit(msg_dict["event"], self)

    @ee.on('keyDown')
    async def key_down_handler(self):
        logging.info("we are here")
        self.mic.toggle_mute()
        if self.mic._volume == 0:
            # send state 1
            pass
        else:
            # send state 2
            pass
