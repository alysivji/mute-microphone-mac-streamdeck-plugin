import asyncio
import logging

from microphone_client import MacMicrophoneClient
from streamdeck import StreamDeckClient

logging.basicConfig(filename="example.log", level=logging.INFO)


class MuteMicrophonePluginManager:
    def __init__(self, args):
        self.microphone = MacMicrophoneClient()
        self.streamdeck = StreamDeckClient(
            port=args.port,
            event=args.event,
            plugin_uuid=args.plugin_uuid,
            info=args.info,
            mic=self.microphone,
        )

    async def connect(self):
        await self.streamdeck.connect_and_listen()

    async def update_input_volume_from_system(self):
        while True:
            await asyncio.sleep(60)
            self.microphone.volume
