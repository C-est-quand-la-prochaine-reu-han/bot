#!/usr/bin/env python

class Coord:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Data:
	def __init__(self):
		self.bot_paddle_pos = Coord(0, 0)
		self.adv_paddle_pos = Coord(0, 0)
		self.ball_speed = Coord(0, 0)
		self.ball_pos = Coord(0, 0)
