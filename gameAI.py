#!/usr/bin/env python

from websockets.asyncio.client import connect
import os
import asyncio
import time
from Bot import Bot

bot = Bot()

async def updateData(data):
	global bot
	if data[0] == "pos":
		bot.real_data.ball_pos.y = int(data[1])
		bot.real_data.ball_pos.x = int(data[2])
	elif data[0] == "mov":
		bot.real_data.ball_speed.y = int(data[1])
		bot.real_data.ball_speed.x = int(data[2])
	elif data[0] == bot.opponent:
		bot.real_data.adv_paddle_pos.y = int(data[1])
		bot.real_data.adv_paddle_pos.x = int(data[2])
	elif data[0] == bot.name:
		bot.real_data.bot_paddle_pos.y = int(data[1])
		bot.real_data.bot_paddle_pos.x = int(data[2])

async def getMessage(websocket):
	while True:
		message = await websocket.recv()
		data = message.split(":")
		await updateData(data)

async def main():
	hostname = os.environ.get("HOSTNAME")
	port = os.environ.get("PORT")
	uri = "wss://" + hostname + ":" + port + "/pong/"

	async with connect(uri) as websocket:

		await websocket.send(bot.name)
		message = await websocket.recv()

		if message == "start":

			message = await websocket.recv()
			data = message.split(":")
			if data[0] == "opponent":
				bot.opponent = data[1]

			message = await websocket.recv()
			data = message.split(":")
			if data[0] == "youare":
				bot.play_side = 2 * int(data[1]) - 3 #invert the playground if we are player 1 

			task = asyncio.create_task(getMessage(websocket))
			bot.bot_view = bot.real_data

			while True:
				next_move = bot.calculateNextMove()
				if next_move is not None:
					await websocket.send(next_move)
				await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())