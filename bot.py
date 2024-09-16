#!/usr/bin/env python

import asyncio
import time

from websockets.asyncio.client import connect


async def hello():
    uri = "ws://localhost:8765"
    async with connect(uri) as websocket:
        name = "BOT"

        await websocket.send(name)
        print(f">>> {name}")

        message = await websocket.recv()
        print(f"<<< {message}")

        if message == "start":
            while True:
                get = await websocket.recv()
                #print(f"<<< {get}")

                message = get.split(":")
                if message[0] == "youare":
                    player = int(message[1])

                if message[0] == "pos":
                    if int(message[-1]) <= 500:
                        await websocket.send("up")
                    elif int(message[-1]) > 500:
                        await websocket.send("down")
                #await asyncio.sleep(1)
                

if __name__ == "__main__":
    asyncio.run(hello())