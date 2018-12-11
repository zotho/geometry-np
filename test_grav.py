#!/usr/bin/env python3

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ListProperty, ReferenceListProperty
from kivy.uix.widget import Widget

import numpy as np

class Planet():
	# Position
	pos = np.array([0., 0.])
	# Velocity
	vel = np.array([0., 0.])
	# Acceleration
	acc = np.array([0., 0.])
	# List [time, pos]
	pos_list = [[0., pos.copy()]]

	def update(self, dt, t):
		self.update_vel(dt, t)
		self.update_pos(dt, t)

	def update_ang(self, dt, t):
		pass

	def update_vel(self, dt, t):
		self.vel = self.vel + (self.acc * dt)

	def update_pos(self, dt, t):
		self.pos = self.pos + (self.vel * dt)

class Space(Widget):
	color = ListProperty([1, 1, 1, .1])
	objects = ReferenceListProperty(None)

	def update(self, dt, t):
		self.canvas.clear()
		for obj in objects:
			obj.update(dt, t)
			'''
			with self.canvas:
			'''

class GravApp(App):
	time = NumericProperty(0)

	def build(self):
		Clock.schedule_interval(self.update, 1/60.)
		self.root = Space()
		return self.root

	def update(self, dt):
		self.time += dt
		self.root.update(dt, self.time)


if __name__ == "__main__":
	GravApp().run()