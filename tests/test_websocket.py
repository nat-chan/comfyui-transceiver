import asyncio
import unittest

import aiohttp

HOST = "localhost"
PORT = 8189


class test_websocket(unittest.TestCase):
    def test_websocket_send(self):
        asyncio.run(self.websocket_send())

    def test_websocket_recieve(self):
        asyncio.run(self.websocket_recieve())

    async def websocket_send(self):
        channel = "test_channel"
        action = "send"
        url = f"http://{HOST}:{PORT}/transceiver?channel={channel}&action={action}"
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(url) as ws:
                data = b"dummy data"
                await ws.send_bytes(data)

    async def websocket_recieve(self):
        channel = "test_channel"
        action = "recieve"
        url = f"http://{HOST}:{PORT}/transceiver?channel={channel}&action={action}"
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(url) as ws:
                await ws.send_bytes(b"")
                response = await ws.receive_bytes()
                print("Received:", response)


if __name__ == "__main__":
    unittest.main()
