#!/usr/bin/env python

import time
from utils import Data

class Bot:
	def __init__(self):
		self.name = "BOT"
		self.opponent = ""
		self.play_side = 0
		self.bot_view = Data()		# View for predictions
		self.real_data = Data()		# Actual data from WebSocket
		self.last_update_time = 0	# Timestamp of the last real update
		self.reaction_time = 0.5	# Reaction delay

	def calculateNextMove(self):
		current_time = time.time()

		# Check if 1 second has passed since the last real data update
		if current_time - self.last_update_time >= 1:
			self.bot_view = self.real_data  # Update with real data
			self.last_update_time = current_time
		else:
			self.predictBallPosition()
		
		# WAIT: If the ball is heading towards the opponent, no need to move
		if not self.isBallHeadingToUs():
			return

		'''
		# ESTIMATE: The ball is returning, but exact position is unknown, add reaction delay
        #           -> lance un timer, quand il sera fini on bouge (temps de reaction du joueur)
		if self.isBallHeadingToUs() and current_time - self.last_update_time < self.reaction_time:
			return
		'''

		# PLAY: The ball is returning, move accordingly
		if self.isBallHeadingToUs():
			if self.isTrajectoryComplex():
				return self.moveToCenter()
			else:
				return self.moveToBall()


	def isBallHeadingToUs(self):
		if self.bot_view.ball_speed.x * self.play_side > 0:
			return True
		return False

	def getTimeBeforeCollision(self):
		time_until_collision = float('inf')

		# Left wall or paddle 
		if self.bot_view.ball_speed.x < 0:
			distance_to_travel = self.bot_view.ball_pos.x - 100  # Distance between border and paddle
			temp_time = abs(distance_to_travel / self.bot_view.ball_speed.x)
			time_until_collision = min(time_until_collision, temp_time)

		# Right wall or paddle 
		elif self.bot_view.ball_speed.x > 0:
			distance_to_travel = 900 - self.bot_view.ball_pos.x - 50  # Size of the ball
			temp_time = abs(distance_to_travel / self.bot_view.ball_speed.x)
			time_until_collision = min(time_until_collision, temp_time)

		# Top wall
		if self.bot_view.ball_speed.y < 0:
			distance_to_travel = self.bot_view.ball_pos.y
			temp_time = abs(distance_to_travel / self.bot_view.ball_speed.y)
			time_until_collision = min(time_until_collision, temp_time)

		# Bottom wall
		elif self.bot_view.ball_speed.y > 0:
			distance_to_travel = 1000 - self.bot_view.ball_pos.y - 50
			temp_time = abs(distance_to_travel / self.bot_view.ball_speed.y)
			time_until_collision = min(time_until_collision, temp_time)

		return time_until_collision

	def predictBallPosition(self):
		delay_until_collision = self.getTimeBeforeCollision()

		# Compute the new position and check for collision
		self.bot_view.ball_pos.x = int(self.bot_view.ball_pos.x + self.bot_view.ball_speed.x * delay_until_collision)
		self.bot_view.ball_pos.y = int(self.bot_view.ball_pos.y + self.bot_view.ball_speed.y * delay_until_collision)


	def isTrajectoryComplex(self):
		"""Check if the ball's trajectory is complex, e.g., many bounces."""
		#How to check the nmber of bounces ?
		return False


	def moveToCenter(self):
		if self.bot_view.bot_paddle_pos.y + 50 < 500:
			return "down"
		elif self.bot_view.bot_paddle_pos.y + 50 > 500:
			return "up"
		return

	def moveToBall(self):
		if abs(self.bot_view.ball_pos.y - (self.bot_view.bot_paddle_pos.y + 50)) < 30:
			return
		if self.bot_view.ball_pos.y < self.bot_view.bot_paddle_pos.y + 50:
			return "up"
		elif self.bot_view.ball_pos.y > self.bot_view.bot_paddle_pos.y + 50:
			return "down"