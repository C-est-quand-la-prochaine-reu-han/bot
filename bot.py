#!/usr/bin/env python

import os
import asyncio
import signal
from GameManager import GameManager

async def shutdown(signal, loop):
    print(f"Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

async def main():
    hostname = os.environ.get("HOSTNAME")
    port = os.environ.get("PORT")
    uri = "wss://" + hostname + ":" + port + "/pong/"

    manager = GameManager(uri)
    manager_task = asyncio.create_task(manager.run())

    await manager_task

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(s, loop)))

    try:
        loop.run_until_complete(main())
    except asyncio.CancelledError:
        pass
    finally:
        loop.close()
