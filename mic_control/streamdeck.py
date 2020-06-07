from dataclasses import dataclass
import json
import logging

from pyee import AsyncIOEventEmitter
import websockets


ee = AsyncIOEventEmitter()


@dataclass
class Device:
    id: str
    name: str
    connected: bool


class StreamDeckClient:
    def __init__(self, port, event, plugin_uuid, info, mic):
        data = json.loads(info)
        self.devices = {
            d["id"]: Device(id=d["id"], name=d["name"], connected=False)
            for d in data["devices"]
        }
        self.plugin_uuid = plugin_uuid
        self.uri = f"ws://localhost:{port}"
        self.registration_info = {"event": event, "uuid": plugin_uuid}
        self.message_queue = []
        self.mic = mic

    async def connect_and_listen(self):
        async with websockets.connect(self.uri) as websocket:
            self.websocket = websocket
            await self.send_to_streamdeck(self.registration_info)
            await self.start_incoming_messages_listener()

    async def send_to_streamdeck(self, payload):
        await self.websocket.send(json.dumps(payload))

    async def start_incoming_messages_listener(self):
        async for message in self.websocket:
            data = json.loads(message)
            logging.info(data)
            ee.emit(data["event"], self, data)

    @ee.on("deviceDidConnect")
    async def device_connected_handler(self, data):
        device_id = data["device"]
        self.devices[device_id].connected = True
        logging.info(f"Device {device_id} connected")

    @ee.on("keyDown")
    async def key_down_handler(self, data):
        logging.info("we are here")
        self.mic.toggle_mute()
        if self.mic._volume == 0:
            # send state 1
            pass
        else:
            # send state 2
            pass
