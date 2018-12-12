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
    def __init__(self, pos=None, vel=None, acc=None, mass=1., num_dimension=2):
        self.num_dimension=num_dimension
        # List [time, pos]
        self.pos_list = []
        self.time_list = []

        self.pos = np.array(pos) if pos else np.array([0.]*self.num_dimension)
        self.vel = np.array(vel) if vel else np.array([0.]*self.num_dimension)
        self.acc = np.array(acc) if acc else np.array([0.]*self.num_dimension)
        self.mass = np.array(mass)
        self.pos_list.append(self.pos.copy())
        self.time_list.append(0.)
        
        self.tail_len = 300
        self.max_tail_len = 1000

    def update_acc(self, dt, t, s):
        self.acc = np.array([0.]*self.num_dimension)
        coll = False
        for obj in s.objects:
            if self is not obj:
                dist = np.linalg.norm(self.pos - obj.pos)
                # print(f"dist = {dist}")
                if dist != 0.:
                    self.acc += (obj.pos - self.pos) * obj.mass * s.grav_const / dist**2
                else:
                    coll = True
                    break   
        if coll:
            s.collide(self, obj)

    def update_vel(self, dt, t):
        self.vel = self.vel + (self.acc * dt)

    def update_pos(self, dt, t):
        self.pos = self.pos + (self.vel * dt)
        self.pos_list.append(self.pos.copy())
        self.time_list.append(t)
        if len(self.pos_list) > self.max_tail_len:
            self.pos_list = self.pos_list[-self.tail_len:]
            self.time_list = self.time_list[-self.tail_len:]


class Space(Widget):
    color = ListProperty([1, 1, 0, .1])

    num_dimension = 3
    def to_num_dimension(self, arr):
        return np.array(list(arr)+[0.]*(self.num_dimension-len(arr))) if len(arr) < self.num_dimension else arr

    objects = []
    touch_start = None
    touch_end = None
    touch_planet = None

    grav_const = 1000.
    inform_speed = 100.

    def sign_log(self, x, m = 10):
        norm = np.linalg.norm(x)
        if norm < 1.:
            norm = 1.
        mult = m * np.log(norm) / norm
        return x * mult

    def rect_size(self, mass, m=10):  
        return np.sqrt(mass) * m, np.sqrt(mass) * m

    def round_size(self, mass, m=3):
        return np.sqrt(mass) * m

    def collide_check(self, p1, p2):
        if len(p1.pos_list) < 2:
            return False
        d = p1.pos_list[-1] - p1.pos_list[-2]
        f = p1.pos_list[-2] - p2.pos

        a = np.dot(d, d)
        b = 2. * np.dot(f, d)
        c = np.dot(f, f) - self.round_size(p2.mass)

        discr = b**2 - 4 * a * c

        if discr < 0:
            return False
        else:
            discr = np.sqrt(discr)
            t1 = (-b - discr) / (2 * a)
            t2 = (-b + discr) / (2 * a)
            if t2 >= 0 and t2 <= 1:
                return True
            return False

    def update(self, dt, t):
        # Update physics
        for obj in self.objects:
            obj.update_acc(dt, t, self)
        for obj in self.objects:
            obj.update_vel(dt, t)
        for obj in self.objects:
            obj.update_pos(dt, t)

        # Updating collide
        while True:
            br = False
            for l in range(len(self.objects)):
                for r in range(l + 1, len(self.objects)):
                    if np.linalg.norm(self.objects[l].pos - self.objects[r].pos) < max(self.round_size(self.objects[l].mass), self.round_size(self.objects[r].mass)):
                        self.collide(self.objects[l], self.objects[r])
                        br = True
                        break
                    elif self.collide_check(self.objects[l], self.objects[r]) or self.collide_check(self.objects[r], self.objects[l]):
                        self.collide(self.objects[l], self.objects[r])
                        br = True
                        break
                if br:
                    break
            else:
                break

        # Drawing
        self.canvas.clear()
        with self.canvas:
            if self.touch_planet:
                self.touch_planet.vel = np.array(self.to_num_dimension([0.]))
                self.touch_planet.pos = np.array(self.to_num_dimension(self.touch_end))
                Color(1, 1, 1, 1)
                Line(points=[self.touch_start[0], self.touch_start[1], 
                             self.touch_end[0], self.touch_end[1]],
                     width=2)
            for obj in self.objects:
                # Tail
                coords = [obj.pos_list[i // self.num_dimension][i % self.num_dimension] for i in range(len(obj.pos_list) * self.num_dimension) if i % self.num_dimension < 2]
                Color(1, 0, 0, .3)
                Line(points=coords[-(obj.tail_len*2):],
                     width=2,
                     joint='round')
                Color(1, 0, 0.5, .3)
                Line(points=coords[-(obj.tail_len//3*4):],
                     width=3,
                     joint='round')
                Color(1, 0, 1, .3)
                # print(f"obj.tail_len = {obj.tail_len}")
                Line(points=coords[-(obj.tail_len//3*2):],
                     width=4,
                     joint='round')
                '''
                #   Debug
                # Vel
                Color(0, 0, 1, 1)
                norm_vel = self.sign_log(obj.vel)
                Line(points=[coords[-2], coords[-1],
                             coords[-2] + norm_vel[0], coords[-1] + norm_vel[1]])
                # Acc
                Color(0, 1, 0, 1)
                norm_acc = self.sign_log(obj.acc)
                # print(f"obj.acc={obj.acc}")
                # print(f"norm_acc={norm_acc}")
                Line(points=[coords[-2], coords[-1],
                             coords[-2] + norm_acc[0], coords[-1] + norm_acc[1]])
                '''
            for obj in self.objects:
                Color(1, 1, 0, 0.9)
                # print(f"obj.mass = {obj.mass}")
                Ellipse(pos=[obj.pos[i]-self.round_size(obj.mass) for i in (0, 1)], size=[self.round_size(obj.mass)*2., self.round_size(obj.mass)*2.])

    def collide(self, p1, p2):
        pos = list((p1.pos * p1.mass + p2.pos * p2.mass) / (p1.mass + p2.mass))
        vel = list((p1.vel * p1.mass + p2.vel * p2.mass) / (p1.mass + p2.mass))
        acc = list(np.array([0.] * self.num_dimension))
        mass = p1.mass + p2.mass
        p3 = Planet(pos=pos, vel=vel, acc=acc, mass=mass, num_dimension=self.num_dimension)
        
        for i in range(len(self.objects)):
            if p1 is self.objects[i]:
                self.objects.pop(i)
                break
        for i in range(len(self.objects)):
            if p2 is self.objects[i]:
                self.objects.pop(i)
                break
        self.objects.append(p3)


    def on_touch_down(self, touch):
        self.touch_start = touch.pos
        self.touch_end = touch.pos
        self.touch_planet = Planet(pos=list(self.to_num_dimension(touch.pos)), mass=1, num_dimension=self.num_dimension)
        self.objects.append(self.touch_planet)

    def on_touch_move(self, touch):
        self.touch_end = touch.pos
        self.touch_planet.pos = np.array(self.to_num_dimension(self.touch_end))

    def on_touch_up(self, touch):
        self.touch_planet.vel = np.array(self.to_num_dimension(self.touch_end)) - np.array(self.to_num_dimension(self.touch_start))
        self.touch_planet = None


class GravApp(App):
    time = NumericProperty(0)

    def build(self):
        Clock.schedule_interval(self.update, 0)
        self.root = Space()
        self.frame = 0
        self.fps_list = []
        return self.root

    def update(self, dt):
        self.dt = dt
        self.time += dt
        self.frame += 1
        self.root.update(dt, self.time)
        self.draw_fps(self.root)

    def draw_fps(self, root):
        fps_max = 40.

        fps = 1. / self.dt

        x = 10
        y = 10
        height = 100
        colors = [(np.sin(fps / fps_max * np.pi - np.pi * i / 2.) + \
                   np.abs(np.sin(fps / fps_max * np.pi - np.pi * i / 2.))) / 2.
                  for i in [1, 2 ,0]]

        self.fps_list.append([fps / fps_max * height, colors])
        self.fps_list = self.fps_list[-100:]

        with root.canvas:
            for i in range(len(self.fps_list)):
                Color(*self.fps_list[i][1], 1)
                Line(points=[x + i * 4, y, x + i * 4, y + self.fps_list[i][0]])


if __name__ == "__main__":
    GravApp().run()