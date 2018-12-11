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

def sign_log(x, m = 10):
    norm = np.linalg.norm(x)
    if norm < 1.:
        norm = 1.
    mult = m * np.log(norm) / norm
    return x * mult

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
        self.acc = np.array((0., 0.))
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
        if len(self.pos_list) > 1000:
            self.pos_list = self.pos_list[-300:]
            self.time_list = self.time_list[-300:]
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
    objects = [Planet(pos=(480, 300),
                      vel=(0, -50),
                      mass=15),
               Planet(pos=(320, 300),
                      vel=(0, 50),
                      mass=15)]
    '''
    objects = []

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
                #for i in range(len(obj.pos_list)):
                coords = [obj.pos_list[i//2][i%2] for i in range(len(obj.pos_list)*2)]
                # print(f"coords={coords}")
                Color(1, 0, 0, .3)
                Line(points=coords[-400:],
                     width=2,
                     joint='round')
                Color(1, 0, 0.5, .3)
                Line(points=coords[-200:],
                     width=3,
                     joint='round')
                Color(1, 0, 1, .3)
                Line(points=coords[-100:],
                     width=4,
                     joint='round')

                # Vel
                Color(0, 0, 1, 1)
                norm_vel = sign_log(obj.vel)
                Line(points=[coords[-2], coords[-1],
                             coords[-2] + norm_vel[0], coords[-1] + norm_vel[1]])
                # Acc
                Color(0, 1, 0, 1)
                norm_acc = sign_log(obj.acc)
                # print(f"obj.acc={obj.acc}")
                # print(f"norm_acc={norm_acc}")
                Line(points=[coords[-2], coords[-1],
                             coords[-2] + norm_acc[0], coords[-1] + norm_acc[1]])
        for obj in self.objects:
            with self.canvas:
                Color(1, 1, 0, 1)
                size = (15, 15)
                Rectangle(pos=[obj.pos[i]-size[i]/2. for i in (0, 1)], size=size)

    def on_touch_down(self, touch):
        self.objects.append(Planet(pos=(touch.pos[0], touch.pos[1]), mass=1))


class GravApp(App):
    time = NumericProperty(0)

    def build(self):
        Clock.schedule_interval(self.update, 0)
        self.root = Space()
        self.frame = 0
        self.rel_time = self.time
        return self.root

    def update(self, dt):
        self.time += dt
        self.frame += 1
        self.root.update(dt, self.time)
        #print(f"fps={self.frame/(self.time-self.rel_time)}")
        if self.frame > 100:
            self.frame = 0
            self.rel_time = float(self.time)


if __name__ == "__main__":
    GravApp().run()