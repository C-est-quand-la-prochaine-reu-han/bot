#!/usr/bin/env python

import os
import ssl
import asyncio
import signal
from websockets import connect
from GameSession import GameSession

async def main():
    sessions = []
    hostname = os.environ.get("PROXY", "localhost")
    port = os.environ.get("PORT", 8443)
    uri = "wss://" + hostname + ":" + port + "/pong/"

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    while True:
        websocket = await connect(uri, ssl=ssl_context)
        await websocket.send("*")
        await websocket.send("BOT")
        message = await websocket.recv()
        if message != "start":
            raise RuntimeError(f"Didn't received start message, instead received {message}")
        new_session = asyncio.create_task(GameSession(websocket).handle_game())
        sessions.append(new_session)
        print("Started new game session number {len(sessions)}")

if __name__ == "__main__":
    asyncio.run(main())
