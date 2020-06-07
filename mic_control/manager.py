import asyncio
import logging

from microphone_client import MacMicrophoneClient
from streamdeck import StreamDeckClient

logging.basicConfig(filename="example.log", level=logging.INFO)


class MuteMicrophonePluginManager:
    def __init__(self, args):
        self.microphone = MacMicrophoneClient(self)
        self.streamdeck = StreamDeckClient(
            manager=self,
            port=args.port,
            event=args.event,
            plugin_uuid=args.plugin_uuid,
            info=args.info,
        )

    async def connect(self):
        await self.streamdeck.connect_and_listen()

    async def update_input_volume_from_system(self):
        while True:
            self.microphone.volume
            await asyncio.sleep(60)

    async def toggle_button(self, context):
        self.microphone.toggle_mute()
        await self._check(context)

    async def _check(self, context):
        set_state = {
            "event": "setState",
            "context": context,
            "payload": {}
        }
        if self.microphone._volume == 0:
            set_state["payload"]["state"] = 1
            await self.streamdeck.send_to_streamdeck(set_state)
        else:
            set_state["payload"]["state"] = 0
            await self.streamdeck.send_to_streamdeck(set_state)
