#!/usr/bin/env python3

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ListProperty, ReferenceListProperty
from kivy.graphics.vertex_instructions import (Rectangle,
                                               Ellipse,
                                               Line)
from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color

import numpy as np

class Planet():
    # Position
    pos = np.array([0, 0])
    # Velocity
    vel = np.array([0., 0.])
    # Acceleration
    acc = np.array([0., 0.])
    # List [time, pos]
    pos_list = [[0., pos.copy()]]

    def __init__(self, pos=pos, vel=vel, acc=acc):
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array(acc)

    '''
    # Bad and had error
    def update(self, dt, t, others):
        self.update_acc(dt, t, others)
        self.update_vel(dt, t)
        self.update_pos(dt, t)
        # print(f"{self.pos},{self.vel},{self.acc}")
    '''

    def update_acc(self, dt, t, others):
        self.acc = 0.
        for obj in others:
            if self is not obj:
                dist = np.linalg.norm(self.pos - obj.pos)
                print(f"dist = {dist}")
                self.acc += (obj.pos - self.pos) * 100 / dist**2

    def update_vel(self, dt, t):
        self.vel = self.vel + (self.acc * dt)

    def update_pos(self, dt, t):
        self.pos = self.pos + (self.vel * dt)

class Space(Widget):
    color = ListProperty([1, 1, 0, .1])
    objects = [Planet(pos=(np.cos(2.*np.pi*i/3.)*10+400,np.sin(2.*np.pi*i/3.)*10+300)) for i in [0,1,2]]

    '''
    def __init__(self):
        n = 3
        self.objects = [Planet(pos=(np.cos(2.*np.pi*i/n)*100+400, 
                                    np.sin(2.*np.pi*i/n)*100+300)) 
                             for i in range(n)]
    '''

    def update(self, dt, t):
        for obj in self.objects:
            obj.update_acc(dt, t, self.objects)
        for obj in self.objects:
            obj.update_vel(dt, t)
        for obj in self.objects:
            obj.update_pos(dt, t)
        self.canvas.clear()
        for obj in self.objects:
            with self.canvas:
                Color(0, 1, 0, 1)
                Rectangle(pos=tuple(obj.pos), size=(5, 5))

class GravApp(App):
    time = NumericProperty(0)

    def build(self):
        Clock.schedule_interval(self.update, 0.)
        self.root = Space()
        return self.root

    def update(self, dt):
        self.time += dt
        self.root.update(dt, self.time)


if __name__ == "__main__":
    GravApp().run()