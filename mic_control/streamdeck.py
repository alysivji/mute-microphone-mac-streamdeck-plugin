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
    context: set


class StreamDeckClient:
    def __init__(self, manager, port, event, plugin_uuid, info):
        self.manager = manager

        data = json.loads(info)
        self.devices = {
            d["id"]: Device(id=d["id"], name=d["name"], connected=False, context=set())
            for d in data["devices"]
        }
        self.plugin_uuid = plugin_uuid
        self.uri = f"ws://localhost:{port}"
        self.registration_info = {"event": event, "uuid": plugin_uuid}

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
        await self.manager.toggle_button()

    @ee.on("willAppear")
    async def will_appear_handler(self, data):
        device_id = data["device"]
        context = data["context"]

        device = self.devices[device_id]
        device.context.add(context)
        await self.manager._update_button()

    async def update_button_state(self, state):
        state_config = {
            "event": "setState",
            "payload": {
                "state": state
            }
        }
        for key, device in self.devices.items():
            if device.connected:
                for app_instance in device.context:
                    state_config["context"] = app_instance
                    await self.send_to_streamdeck(state_config)
