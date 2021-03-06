#!/usr/bin/env python3

import numpy as np

from collections import deque

class Planet():
    __slots__ = 'num_dimension', 'pos', 'vel', 'acc', 'mass', 'collided', \
                'tail', 'tail_len', 'tail_time', 'tail_back', 'tail_coords'

    def __init__(self, pos=None, vel=None, acc=None, mass=1., num_dimension=2, tail_len=300, tail_time=1., tail_back=0):
        self.num_dimension = num_dimension

        self.pos = np.array(pos) if pos else np.array([0.]*self.num_dimension)
        self.vel = np.array(vel) if vel else np.array([0.]*self.num_dimension)
        self.acc = np.array(acc) if acc else np.array([0.]*self.num_dimension)
        self.mass = np.array(mass)
        self.collided = False
        
        # Tail
        self.tail_back = tail_back
        self.tail_len = tail_len
        self.tail_time = tail_time
        self.tail = deque(maxlen=tail_len)
        self.tail.appendleft((self.pos.copy(), 0.))
        self.tail_coords = deque(maxlen=tail_len*2)
        self.tail_coords.extendleft(self.pos[1::-1])

    def update_acc(self, dt, s):
        self.acc.fill(0.)
        for obj in s.objects:
            if self is not obj:
                dist = np.linalg.norm(self.pos - obj.pos)
                if not(dist < self.round_size() + obj.round_size() or \
                        self.collide_check(obj)):
                    self.acc += (obj.pos - self.pos) * obj.mass * s.grav_const / dist**2
                else:
                    self.collided = obj
                    break

    def update_vel(self, dt):
        self.vel += self.acc * dt

    def update_pos(self, dt):
        self.pos += self.vel * dt
        pos = self.pos
        tail = self.tail
        new_dt = dt + tail[0][1]
        if new_dt < self.tail_time / self.tail_len:
            self.tail[0] = (tail[0][0], new_dt)
        else:
            self.tail.appendleft((pos.copy(), dt))
            self.tail_coords.appendleft(pos[1])
            self.tail_coords.appendleft(pos[0])
            if self.tail_back > 0:
                self.tail_back -= 2

    def round_size(self, m=3.):
        return self.mass**.5 * m

    def collide_check(self, obj):
        tail = self.tail
        if len(tail) < 2:
            return False

        first = tail[0][0]
        second = tail[1][0]
        d = first - second
        f = second - obj.pos

        a = np.dot(d, d)
        b = 2. * np.dot(f, d)
        c = np.dot(f, f) - obj.round_size()

        discr = b**2 - 4. * a * c

        if discr < 0. or a == 0.:
            return False
        else:
            discr = discr**.5
            t1 = (-b - discr) / (2. * a)
            t2 = (-b + discr) / (2. * a)
            if t2 >= 0. and t2 <= 1.:
                return True
            return False
