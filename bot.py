#!/usr/bin/env python

import os
import ssl
import asyncio
import signal
from websockets import connect
from GameSession import GameSession

async def main():
    hostname = os.environ.get("PROXY", "localhost")
    port = os.environ.get("PORT", 8443)
    uri = "wss://" + hostname + ":" + port + "/pong/"

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    while True:
        async with connect(uri, ssl=ssl_context) as websocket:
            session = GameSession(websocket)
            session_task = asyncio.create_task(session.handle_game())
            print("Started new game session")
            await session_task

if __name__ == "__main__":
    asyncio.run(main())
