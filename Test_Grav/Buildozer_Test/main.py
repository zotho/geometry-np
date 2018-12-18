#!/usr/bin/env python3

from kivy.app import App                # main app
from kivy.clock import Clock            # for event loop
from kivy.core.window import Window     # for keyboard

from space import Space                 # Space class
from fps import Fps                     # Fps meter

class GravApp(App):

    def build(self):

        self.draw_fps = True
        self.fps = Fps()

        self.time = 0.
        self.last_time = 0.

        Clock.schedule_interval(self.update, 0)

        self.root = Space()
        return self.root

    def update(self, dt):

        self.dt = dt
        self.time += dt

        if self.time - self.last_time >= 1.:
            self.last_time = self.time
            print(Clock.get_fps())

        self.root.update(dt, self.time)

        if self.draw_fps:
            self.fps.update(dt)
            self.fps.draw(self.root)

if __name__ == "__main__":
    GravApp().run()