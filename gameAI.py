#!/usr/bin/env python

from websockets.asyncio.client import connect
import asyncio
import time
import Bot

bot = Bot()

async def updateData(data):
	global bot
	if data[0] == "pos":
		bot.real_data.ball_pos.x = int(data[1])
		bot.real_data.ball_pos.y = int(data[2])
	elif data[0] == "mov":
		bot.real_data.ball_speed.x = int(data[1])
		bot.real_data.ball_speed.y = int(data[2])

async def getMessage(websocket):
	while True:
		message = await websocket.recv()
		print(message)
		data = message.split(":")
		await updateData(data)

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
			bot.bot_view = bot.real_data
			while True:
				next_move = bot.calculateNextMove()
				await websocket.send(next_move)
				await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())