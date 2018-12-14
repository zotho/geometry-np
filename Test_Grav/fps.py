#!/usr/bin/env python3

from kivy.graphics.vertex_instructions import (Rectangle,
                                               Ellipse,
                                               Line)
from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color

from math import sin, pi
from collections import deque

class Fps():
    '''f = fps(x=50., y=50., height=30., width=200., time=5., fps_max=40.)

    '''
    def __init__(self, x=50., y=50., height=30., width=200., time=5., fps_max=40.):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.time = time        
        self.fps_max = fps_max

        # ???
        self.max_dt = time / width * 5.

        self.data = deque(maxlen=int(time * fps_max))
        self.data.appendleft((self.fps_max, 0., (1., 0., 0.)))

    def update(self, dt):
        data = self.data

        # ??? Need? Test in timeit!
        first = data[0]

        fps = 1. / dt

        first_dt = first[1]
        first_fps = first[0]
        
        new_dt = dt + first_dt

        colr = self._color
        fps_max = self.fps_max
        
        if new_dt < self.max_dt:
            data[0] = ((fps * dt + first_fps * first_dt) / new_dt,
                       new_dt,
                       (0., 0., 0., 0.))
        else:
            data[0] = (first_fps,
                       first_dt,
                       colr(first_fps, fps_max))
            data.appendleft((fps, dt, (0., 0., 0., 0.)))

    def _color(self, fps, fps_max):
        return tuple(((sin(fps / fps_max * pi - pi * i / 2.) + \
                       abs(sin(fps / fps_max * pi - pi * i / 2.))) / 2.
                      for i in (1, 2 ,0)))

    def draw(self, root):
        x = self.x
        y = self.y
        height = self.height
        width = self.width
        time = self.time        
        fps_max = self.fps_max
        data = self.data

        t = 0.

        t_xi = None
        t_yi = None

        with root.canvas:
            for fps, dt, colr in data:
                t += dt
                xi = x + t / time * width
                yi = y + fps / fps_max * height
                Color(*colr, 1.)
                # print(f'Color({[i for i in  colr]})')
                if t_xi and t_yi:
                    Line(points=[t_xi, t_yi, xi, yi])
                t_xi = xi
                t_yi = yi
                if t > time:
                    break