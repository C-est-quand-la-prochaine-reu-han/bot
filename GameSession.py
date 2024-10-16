#!/usr/bin/env python

import sys
import asyncio
from PongBot import PongBot

class GameSession:
    def __init__(self, websocket):
        self.bot = PongBot()
        self.websocket = websocket
        self.message_task = None

    async def updateData(self, data):
        if data[0] == "pos":
            self.bot.real_data.ball_pos.y = float(data[1])
            self.bot.real_data.ball_pos.x = float(data[2])
        elif data[0] == "mov":
            self.bot.real_data.ball_speed.y = float(data[1])
            self.bot.real_data.ball_speed.x = float(data[2])
        elif data[0] == self.bot.opponent:
            self.bot.real_data.adv_paddle_pos.y = float(data[1])
            self.bot.real_data.adv_paddle_pos.x = float(data[2])
        elif data[0] == "BOT":
            self.bot.real_data.bot_paddle_pos.y = float(data[1])
            self.bot.real_data.bot_paddle_pos.x = float(data[2])

    async def getMessage(self):
        try:
            async for message in self.websocket:
                data = message.split(":")
                await self.updateData(data)
        except asyncio.CancelledError:
            print(f"getMessage cancelled.")
        except Exception as e:
            print(f"Error in getMessage: {e}")

    async def handle_game(self):
        try:
            await self.websocket.send("BOT")
            message = await self.websocket.recv()
            if message != "start":
                raise RuntimeError(f"Didn't received start message, instead received {message}")

            message = await self.websocket.recv()
            data = message.split(":")
            if data[0] != "opponent":
                raise RuntimeError(f"Didn't received opponent message, instead received {message}")
            self.bot.opponent = data[1]

            message = await self.websocket.recv()
            data = message.split(":")
            if data[0] != "youare":
                raise RuntimeError(f"Didn't received youare message, instead received {message}")
            self.bot.play_side = 2 * int(data[1]) - 3  # Invert the playground if bot is player 1

            self.message_task = asyncio.create_task(self.getMessage())
            self.bot.bot_view = self.bot.real_data

            while True:
                next_move = self.bot.calculateNextMove()
                if next_move is not None:
                    await self.websocket.send(next_move)
                await asyncio.sleep(0.1)

        except asyncio.CancelledError:
            print(f"Game session cancelled.")
            if self.message_task:
                self.message_task.cancel()
        except Exception as e:
            print(f"Error game session: {e}")
            if self.message_task:
                self.message_task.cancel()
