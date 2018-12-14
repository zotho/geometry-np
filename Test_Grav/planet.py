#!/usr/bin/env python3

import numpy as np

class Planet():
    def __init__(self, pos=None, vel=None, acc=None, mass=1., num_dimension=2):
        self.num_dimension = num_dimension

        self.pos = np.array(pos) if pos else np.array([0.]*self.num_dimension)
        self.vel = np.array(vel) if vel else np.array([0.]*self.num_dimension)
        self.acc = np.array(acc) if acc else np.array([0.]*self.num_dimension)
        self.mass = np.array(mass)
        
        # Tail
        # TODO tail.py
        self.pos_list = []
        self.time_list = []
        self.tail_len = 300
        self.max_tail_len = 1000

        self.pos_list.append(self.pos.copy())
        self.time_list.append(0.)
        # !!!!

    def update_acc(self, dt, t, s):
        self.acc.fill(0.)
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
            # !!! Deletes this instanse
            # TODO self.collided = True and check it in Space class
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
        # TODO check collide THERE !!!!

    def round_size(self, m=3.):
        return (self.mass ** .5) * m