import json
import logging

import websockets

logging.basicConfig(filename="example.log", level=logging.INFO)


async def handle_messages(websocket):
    async for message in websocket:
        msg_dict = json.loads(message)
        logging.info(msg_dict)


async def connect_and_listen(registration_info: dict, port: int):
    uri = f"ws://localhost:{port}"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(registration_info))
        await handle_messages(websocket)
