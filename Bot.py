#!/usr/bin/env python

import time
from utils import Data

'''
class Bot:
	name = "BOT"
	opponent = ""
	play_side = 0
	bot_view = Data()
	real_data = Data()

	def calculateNextMove(self):
		#WAIT -> la balle va rebondir sur le paddle adverse -> ne bouge pas
		#ESTIMATE -> la balle revient mais on ne connait pas sa position -> lance un timer, quand il sera fini on bouge (temps de reaction du joueur)
		#PLAY -> la balle revient et on connait sa position -> si trop de rebond va au milieu; sinon va sur la balle si n'y est pas deja
'''

class Bot:
	name = "BOT"
	opponent = ""
	play_side = 0
	bot_view = Data()  # View for predictions
	real_data = Data()  # Actual data from WebSocket

	last_update_time = 0  # Timestamp of the last real update
	reaction_time = 0.5  # Reaction delay

	def calculateNextMove(self):
		current_time = time.time()

		# WAIT: If ball is heading towards the opponent, no need to move
		if self.isBallHeadingToOpponent():
			return

		# ESTIMATE: The ball is returning, but exact position is unknown
		if not self.isBallReturning() and current_time - self.last_update_time < self.reaction_time:
			return
			# Check if 0 second has passed since the last real data update
			if current_time - self.last_update_time >= 0:
				self.updateViewWithRealData()  # Update with real data
			else:
				self.predictBallPosition()  # Predict ball movement

		# PLAY: The ball is returning, move accordingly
		if self.isBallReturning():
			if self.isBallTrajectoryComplex():
				return self.moveToCenter()
			else:
				return self.moveToBall()

	def updateViewWithRealData(self):
		"""Update the bot's view with real data from the game."""

	def predictBallPosition(self):
		"""Predict the ball's position based on speed and time elapsed since last update."""

	def isBallHeadingToOpponent(self):
		"""Check if the ball is moving towards the opponent's side."""

	def isBallReturning(self):
		"""Check if the ball is coming back to the bot's side."""

	def isBallTrajectoryComplex(self):
		"""Check if the ball's trajectory is complex, e.g., many bounces."""

	def moveToCenter(self):
		"""Move the paddle to the center."""

	def moveToBall(self):
		"""Move the paddle towards the ball."""