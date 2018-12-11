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

    def __init__(self, pos=[0., 0.], vel=[0., 0.], acc=[0., 0.], mass=1.):
        # List [time, pos]
        self.pos_list = []
        self.time_list = []

        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array(acc)
        self.mass = np.array(mass)
        self.pos_list.append(self.pos.copy())
        self.time_list.append(0.)

    '''
    # Bad and had error
    def update(self, dt, t, others):
        self.update_acc(dt, t, others)
        self.update_vel(dt, t)
        self.update_pos(dt, t)
        # print(f"{self.pos},{self.vel},{self.acc}")
    '''

    def update_acc(self, dt, t, s):
        self.acc = 0.
        for obj in s.objects:
            if self is not obj:
                dist = np.linalg.norm(self.pos - obj.pos)
                # print(f"dist = {dist}")
                self.acc += (obj.pos - self.pos) * obj.mass * s.grav_const / dist**2

    def update_vel(self, dt, t):
        self.vel = self.vel + (self.acc * dt)

    def update_pos(self, dt, t):
        self.pos = self.pos + (self.vel * dt)
        self.pos_list.append(self.pos.copy())
        self.time_list.append(t)
        # print(f"self.pos_list={self.pos_list}")
        # print(self.pos_list)


class Space(Widget):
    color = ListProperty([1, 1, 0, .1])
    '''
    objects = [Planet(pos=(np.cos(2.*np.pi*i/2.)*50+400,
                           np.sin(2.*np.pi*i/2.)*50+300),
                      vel=(np.cos(2.*np.pi*i/2.+np.pi/2)*10,
                           np.sin(2.*np.pi*i/2.+np.pi/2)*10)
                      ) 
               for i in [0,1]]
    '''
    objects = [Planet(pos=(400, 300),
                      vel=(0, -1),
                      mass=10.),
               Planet(pos=(200, 300),
                      vel=(0, 10),
                      mass=1.)]

    grav_const = 1000.
    inform_speed = 100.
    '''
    def __init__(self):
        n = 3
        self.objects = [Planet(pos=(np.cos(2.*np.pi*i/n)*100+400, 
                                    np.sin(2.*np.pi*i/n)*100+300)) 
                             for i in range(n)]
    '''

    def update(self, dt, t):
        for obj in self.objects:
            obj.update_acc(dt, t, self)
        for obj in self.objects:
            obj.update_vel(dt, t)
        for obj in self.objects:
            obj.update_pos(dt, t)
        self.canvas.clear()
        for obj in self.objects:
            with self.canvas:
                # print(f"obj.pos_list={list(obj.pos_list)}")
                Color(0, 1, 0, .6)
                #for i in range(len(obj.pos_list)):
                coords = [obj.pos_list[i//2][i%2] for i in range(len(obj.pos_list)*2)]
                # print(f"coords={coords}")

                Line(points=coords,
                     width=2,
                     joint='round')
        for obj in self.objects:
            with self.canvas:
                Color(1, 0, 0, 1)
                size = (10, 10)
                Rectangle(pos=[obj.pos[i]-size[i]/2. for i in (0, 1)], size=size)

class GravApp(App):
    time = NumericProperty(0)

    def build(self):
        Clock.schedule_interval(self.update, 0)
        self.root = Space()
        return self.root

    def update(self, dt):
        self.time += dt
        self.root.update(dt, self.time)


if __name__ == "__main__":
    GravApp().run()