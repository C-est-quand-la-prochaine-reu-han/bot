#!/usr/bin/env python

import asyncio
from websockets import connect
from GameSession import GameSession

class GameManager:
    def __init__(self, uri):
        self.uri = uri
        self.active_sessions = {}
        self.session_counter = 0

    async def listen_for_new_games(self):
        async with connect(self.uri) as websocket:
            async for message in websocket:
                if message == "start":
                    bot_name = "Bot" + self.session_counter
                    self.session_counter += 1
                    session = GameSession(self.uri, bot_name)
                    task = asyncio.create_task(session.handle_game())
                    self.active_sessions[bot_name] = task

                    print(f"Started new game session: {bot_name}")

    async def run(self):
        await self.listen_for_new_games()
