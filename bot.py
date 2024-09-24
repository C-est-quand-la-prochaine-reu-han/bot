#!/usr/bin/env python

import asyncio
import time

from websockets.asyncio.client import connect


class Coord:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Data:
	bot_paddle_pos = Coord(0, 0)
	adv_paddle_pos = Coord(0, 0)
	ball_speed = Coord(0, 0)
	ball_pos = Coord(0, 0)

class Bot:
	name = "BOT"
	opponent = ""
	play_side = 0
	bot_view = Data()
	real_data = Data()

	def calculateNextMove(self):
		if self.bot_view.ball_pos.y < 500:
			return "up"
		else:
			return "down"


bot = Bot()

async def updateData(data):
	global bot
	if data[0] == "pos":
		bot.real_data.ball_pos.x = int(data[1])
		bot.real_data.ball_pos.y = int(data[2])
	elif data[0] == "mov":
		bot.real_data.ball_speed.x = int(data[1])
		bot.real_data.ball_speed.y = int(data[2])
	elif data[0] == bot.opponent:
		bot.real_data.adv_paddle_pos.x = int(data[1])
		bot.real_data.adv_paddle_pos.y = int(data[2])
	elif data[0] == bot.name:
		bot.real_data.bot_paddle_pos.x = int(data[1])
		bot.real_data.bot_paddle_pos.y = int(data[2])


async def getMessage(websocket):
	message = await websocket.recv()
	data = message.split(":")
	updateData(data)


async def main():
	uri = "ws://localhost:8765"
	async with connect(uri) as websocket:

		await websocket.send(bot.name)
		message = await websocket.recv()

		if message == "start":
			message = await websocket.recv()
			data = message.split(":")
			if data[0] == "youare":
				bot.play_side = int(data[1])
			message = await websocket.recv()
			data = message.split(":")
			if data[0] == "opponent":
				bot.opponent = data[1]

			task = asyncio.create_task(getMessage(websocket))
			while True:
				next_move = bot.calculateNextMove()
				await websocket.send(next_move)


if __name__ == "__main__":
    asyncio.run(main())