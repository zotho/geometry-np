#!/usr/bin/env python3

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.context_instructions import Color

from space import Space
from fps import Fps

from math import sin, pi


class GravApp(App):
    time = NumericProperty(0)

    def build(self):
        Clock.schedule_interval(self.update, 0)
        self.root = Space()
        self.fps = Fps()
        return self.root

    def update(self, dt):
        self.dt = dt
        self.time += dt
        self.root.update(dt, self.time)
        self.fps.update(dt)
        self.fps.draw(self.root)

if __name__ == "__main__":
    GravApp().run()