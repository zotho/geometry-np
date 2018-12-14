#!/usr/bin/env python3

from kivy.uix.widget import Widget
from kivy.graphics.vertex_instructions import (Line, Ellipse)
from kivy.graphics.context_instructions import Color

import numpy as np

from math import log

from planet import Planet 

class Space(Widget):

    num_dimension = 3
    def to_num_dimension(self, arr):
        return np.array(list(arr) + [0.]*(self.num_dimension - len(arr))) \
               if len(arr) < self.num_dimension \
               else arr

    objects = []
    touch_start = None
    touch_end = None
    touch_planet = None

    grav_const = 1000.
    inform_speed = 100.

    def sign_log(self, x, m = 10.):
        '''Normalise vector(np array) by log of it length

        '''
        norm = np.linalg.norm(x)
        if norm < 1.:
            norm = 1.
        return m * log(norm) / norm * x

    '''
    def rect_size(self, mass, m=10.):  
        return ((mass ** .5) * m,) * 2
    '''

    def collide_check(self, p1, p2):
        if len(p1.pos_list) < 2:
            return False
        d = p1.pos_list[-1] - p1.pos_list[-2]
        f = p1.pos_list[-2] - p2.pos

        a = np.dot(d, d)
        b = 2. * np.dot(f, d)
        c = np.dot(f, f) - p2.round_size()

        discr = b**2 - 4 * a * c

        if discr < 0:
            return False
        else:
            discr = discr ** .5
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
                    if np.linalg.norm(self.objects[l].pos - \
                                      self.objects[r].pos) < \
                       max(self.objects[l].round_size(), 
                           self.objects[r].round_size()):
                        br = True
                        break
                    elif self.collide_check(self.objects[l], 
                                            self.objects[r]) or \
                         self.collide_check(self.objects[r], self.objects[l]):
                        br = True
                        break
                if br:
                    self.collide(self.objects[l], self.objects[r])
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
                # TODO new Tail
                coords = [obj.pos_list[i // self.num_dimension][i % self.num_dimension]
                          for i in range(len(obj.pos_list) * self.num_dimension)
                          if i % self.num_dimension < 2]
                Color(1, 0, 0, .3)
                Line(points=coords[-(obj.tail_len * 2):],
                     width=2,
                     joint='round')
                Color(1, 0, 0.5, .3)
                Line(points=coords[-(obj.tail_len//3 * 4):],
                     width=3,
                     joint='round')
                Color(1, 0, 1, .3)
                Line(points=coords[-(obj.tail_len//3 * 2):],
                     width=obj.round_size(),
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
                r_size = obj.round_size()
                Ellipse(pos=[obj.pos[i] - r_size for i in (0, 1)], size=[r_size*2., r_size*2.])

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
        self.touch_planet = Planet(pos=list(self.to_num_dimension(touch.pos)),
                                   mass=1, 
                                   num_dimension=self.num_dimension)
        self.objects.append(self.touch_planet)

    def on_touch_move(self, touch):
        self.touch_end = touch.pos
        self.touch_planet.pos = np.array(self.to_num_dimension(self.touch_end))

    def on_touch_up(self, touch):
        self.touch_planet.vel = np.array(self.to_num_dimension(self.touch_end)) - \
                                np.array(self.to_num_dimension(self.touch_start))
        self.touch_planet = None