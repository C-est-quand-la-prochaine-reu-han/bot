#!/usr/bin/env python

import asyncio
from websockets import connect
from PongBot import PongBot

class GameSession:
    def __init__(self, uri, bot_name):
        self.uri = uri
        self.bot = PongBot(bot_name)
        self.websocket = None
        self.listener_task = None

    async def updateData(self, data):
        if data[0] == "pos":
            self.bot.real_data.ball_pos.y = int(data[1])
            self.bot.real_data.ball_pos.x = int(data[2])
        elif data[0] == "mov":
            self.bot.real_data.ball_speed.y = int(data[1])
            self.bot.real_data.ball_speed.x = int(data[2])
        elif data[0] == self.bot.opponent:
            self.bot.real_data.adv_paddle_pos.y = int(data[1])
            self.bot.real_data.adv_paddle_pos.x = int(data[2])
        elif data[0] == self.bot.name:
            self.bot.real_data.bot_paddle_pos.y = int(data[1])
            self.bot.real_data.bot_paddle_pos.x = int(data[2])

    async def getMessage(self):
        try:
            async for message in self.websocket:
                data = message.split(":")
                await self.updateData(data)
        except asyncio.CancelledError:
            print(f"Listener task for {self.bot.name} cancelled.")
        except Exception as e:
            print(f"Error in listener for {self.bot.name}: {e}")

    async def handle_game(self):
        try:
            async with connect(self.uri) as websocket:
                self.websocket = websocket
                await self.websocket.send(self.bot.name)
                message = await self.websocket.recv()

                if message == "start":
                    message = await self.websocket.recv()
                    data = message.split(":")
                    if data[0] == "opponent":
                        self.bot.opponent = data[1]

                    message = await self.websocket.recv()
                    data = message.split(":")
                    if data[0] == "youare":
                        self.bot.play_side = 2 * int(data[1]) - 3  # Invert the playground if bot is player 1

                    # Start listening for messages in the background
                    self.listener_task = asyncio.create_task(self.getMessage())

                    self.bot.bot_view = self.bot.real_data

                    while True:
                        next_move = self.bot.calculateNextMove()
                        if next_move is not None:
                            await self.websocket.send(next_move)
                        await asyncio.sleep(0.1)

        except asyncio.CancelledError:
            print(f"Game session for {self.bot.name} cancelled.")
            if self.listener_task:
                self.listener_task.cancel()
        except Exception as e:
            print(f"Error in game session for {self.bot.name}: {e}")
            if self.listener_task:
                self.listener_task.cancel()
