from .utilities import FakeMicrophoneClient
from mic_control.streamdeck import StreamDeckClient


INFO_FROM_COMMAND_LINE = {
    "application": {"language": "en", "platform": "mac", "version": "4.7.0.12981"},
    "devicePixelRatio": 2,
    "devices": [
        {
            "id": "A123",
            "name": "Stream Deck",
            "size": {"columns": 5, "rows": 3},
            "type": 0,
        },
        {"id": "D453", "name": "iPhone", "size": {"columns": 5, "rows": 3}, "type": 3},
    ],
    "plugin": {"version": "1.4"},
}


class TestStreamDeckClient:
    def test_initaialization(self):
        mic = FakeMicrophoneClient()
        client = StreamDeckClient(
            port=123,
            event="registerPlugin",
            plugin_uuid="abc123",
            info=INFO_FROM_COMMAND_LINE,
            mic=mic,
        )

        assert len(client.devices) == 2
        device = client.devices[0]
        assert device.id == "A123"
        assert device.name == "Stream Deck"

        device = client.devices[1]
        assert device.id == "D453"
        assert device.name == "iPhone"
