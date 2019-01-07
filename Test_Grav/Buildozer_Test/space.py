#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.effectwidget import EffectWidget, HorizontalBlurEffect, VerticalBlurEffect, FXAAEffect
from kivy.graphics.vertex_instructions import (Line, Ellipse)
from kivy.graphics.context_instructions import Color

import numpy as np
from mgen import rotation_from_angle_and_plane

from math import log

from planet import Planet

class Space(EffectWidget):
    #   Not working
    # effects: ew.HorizontalBlurEffect(size=0.1), ew.VerticalBlurEffect(size=0.1), ew.FXAAEffect()
    
    __slots__ = 'num_dimension', 'objects', 'tails', \
                'touch_start', 'touch_end', 'touch_planet', \
                'show_acc', 'show_vel', \
                'grav_const', 'inform_speed'


    def __init__(self, **kwargs):
        super(Space, self).__init__(**kwargs)

        # self.effects = [HorizontalBlurEffect(size=0.1),]

        self.num_dimension = 3
        self.objects = []

        self.tails = []

        self.touch_start = None
        self.touch_end = None
        self.touch_planet = None

        self.show_acc = False
        self.show_vel = False

        self.grav_const = 1000.
        self.inform_speed = 100. # not used


    def to_num_dimension(self, arr, up=0):
        num = self.num_dimension + up
        if isinstance(arr, (list, tuple)):
            new_arr = np.array(arr)
        else:
            new_arr = arr.copy()

        new_arr.resize(num)
        return new_arr
        '''
        return np.array(list(arr) + [0.]*(self.num_dimension - len(arr))) \
               if len(arr) < self.num_dimension \
               else arr
        '''

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

    def update(self, dt, t):
        # Update physics
        while True:
            for obj in self.objects:
                obj.update_acc(dt, self)
                if obj.collided:
                    self.collide(obj, obj.collided, t)
                    break
            else:
                break
        for obj in self.objects:
            obj.update_vel(dt)
        for obj in self.objects:
            obj.update_pos(dt)

        # Drawing
        self.canvas.clear()
        with self.canvas:
            if self.touch_planet:
                self.touch_planet.vel = self.to_num_dimension([0.])
                self.touch_planet.pos = self.to_num_dimension(self.touch_end)
                Color(1, 1, 1, .6)
                Line(points=[self.touch_start[0], self.touch_start[1], 
                             self.touch_end[0], self.touch_end[1]],
                     width=2)
            # print(f'len_tails = {len(self.tails)}')
            for tail in self.tails:
                if tail[1] + 2 == tail[2]:
                    self.tails.remove(tail)
                    continue

                coords = list(tail[0])

                Color(1, .0, .0, .3)
                Line(points=coords,
                     width=2,
                     joint='round')

                Color(1., .0, .5, .3)
                len_coords1 = (tail[2] * 2 // 3) // 2 * 2
                if len_coords1 - tail[1] > 2:
                    if len_coords1 < 2:
                        len_coords1 = 2
                    Line(points=coords[:len_coords1 - tail[1]],
                         width=tail[3] / 2.,
                         joint='round')
                
                Color(1., .0, .6, .5)
                len_coords1 = (tail[2] // 3) // 2 * 2
                if len_coords1 - tail[1] > 2:
                    if len_coords1 < 2:
                        len_coords1 = 2
                    Line(points=coords[:len_coords1 - tail[1]],
                         width=tail[3],
                         joint='round')

                # print(f'tail = {tail}')
                tail[0].pop()
                tail[0].pop()
                tail[1] += 2

            for obj in self.objects:
                # Tail
                # TODO new Tail
                coords = list(obj.tail_coords)
                len_coords = len(coords)
                if len_coords < 2:
                    continue
                
                Color(1, 0, 0, .3)
                Line(points=coords,
                     width=2,
                     joint='round')
                
                Color(1, 0, 0.5, .3)
                len_coords1 = (len_coords * 2 // 3) // 2 * 2 + obj.tail_back
                if len_coords1 < 2:
                    len_coords1 = 2
                Line(points=coords[:len_coords1],
                     width=obj.round_size() / 2.,
                     joint='round')
                
                Color(1, 0, .6, .5)
                len_coords1 = (len_coords // 3) // 2 * 2 + obj.tail_back
                if len_coords1 < 2:
                    len_coords1 = 2
                Line(points=coords[:len_coords1],
                     width=obj.round_size(),
                     joint='round')


            for obj in self.objects:
                Color(1, 1, 0, 0.9)
                r_size = obj.round_size()
                Ellipse(pos=[obj.pos[i] - r_size for i in (0, 1)], size=[r_size*2., r_size*2.])

            sum_pos = self.to_num_dimension([0.])
            sum_vel = self.to_num_dimension([0.])
            sum_acc = self.to_num_dimension([0.])
            sum_mass = 0.
            # Debug
            if self.show_vel or self.show_acc:
                for obj in self.objects:
                    sum_acc += obj.acc * obj.mass # must be == 0
                    sum_vel += obj.vel * obj.mass
                    sum_pos += obj.pos * obj.mass
                    sum_mass += obj.mass

                    if self.show_vel:
                        Color(0, 0, 1, 1)
                        # norm_vel = self.sign_log(obj.vel)
                        norm_vel = obj.vel
                        Line(points=(obj.pos[0], obj.pos[1],
                                     obj.pos[0] + norm_vel[0], obj.pos[1] + norm_vel[1]))
                    if self.show_acc:
                        Color(0, 1, 0, 1)
                        norm_acc = self.sign_log(obj.acc)
                        Line(points=(obj.pos[0], obj.pos[1],
                                     obj.pos[0] + norm_acc[0], obj.pos[1] + norm_acc[1]))

                sum_pos = sum_pos / sum_mass if sum_mass != 0. else self.to_num_dimension([0.])
                sum_vel = sum_vel / sum_mass if sum_mass != 0. else self.to_num_dimension([0.])
                sum_acc = sum_acc / sum_mass if sum_mass != 0. else self.to_num_dimension([0.])

                # Sum position mark
                mark_size = 10.
                Color(1, 0, 0, 1)
                # print(f'sum_pos = {sum_pos}\nsum_vel = {sum_vel}\nsum_acc = {sum_acc}\n')
                Line(points=(sum_pos[0], sum_pos[1] - mark_size, \
                             sum_pos[0], sum_pos[1] + mark_size))
                Line(points=(sum_pos[0] - mark_size, sum_pos[1], \
                             sum_pos[0] + mark_size, sum_pos[1]))
                # Sum vel
                Color(0, 0, 1, 1)
                Line(points=(sum_pos[0], sum_pos[1], \
                             sum_pos[0] + sum_vel[0], sum_pos[1] + sum_vel[1]))
                # Sum acc
                Color(0, 0, 1, 1)
                Line(points=(sum_pos[0], sum_pos[1],
                             sum_pos[0] + sum_acc[0], sum_pos[1] + sum_acc[1]))

    def set_vel(self, end_vel):
        sum_vel = self.to_num_dimension([0.])
        sum_mass = 0.
        for obj in self.objects:
            sum_vel += obj.vel * obj.mass
            sum_mass += obj.mass

        sum_vel = sum_vel if sum_mass != 0. else self.to_num_dimension([0.])

        dvel = self.to_num_dimension(end_vel) * sum_mass - sum_vel

        '''
        print('')
        print(sum_vel)
        print(dvel)
        '''

        for obj in self.objects:
            obj.vel = obj.vel + dvel / sum_mass

    def set_pos(self, end_pos):
        sum_pos = self.to_num_dimension([0.])
        sum_mass = 0.
        for obj in self.objects:
            sum_pos += obj.pos * obj.mass
            sum_mass += obj.mass

        sum_pos = sum_pos / sum_mass if sum_mass != 0. else self.to_num_dimension([0.])

        dpos = self.to_num_dimension(end_pos) - sum_pos

        for obj in self.objects:
            obj.pos = obj.pos + dpos

    def rotate(self, angle, vector1, vector2, rot_point):
        tnd = self.to_num_dimension

        num = self.num_dimension + 1

        rot_pos = tnd(rot_point).reshape(num - 1, 1)

        matrix_translate = np.eye(num)
        matrix_translate[0:num-1, num-1:num] = rot_pos * -1.

        matrix_rot = rotation_from_angle_and_plane(angle,
                                                   tnd(vector1, up=1),
                                                   tnd(vector2, up=1))

        matrix_from_origin = matrix_rot.copy()

        matrix_rot = np.dot(matrix_rot, matrix_translate)

        matrix_translate[0:num-1, num-1:num] = rot_pos

        matrix_rot = np.dot(matrix_translate, matrix_rot)

        # print(matrix_rot)

        for obj in self.objects:
            obj.rotate(matrix_rot, matrix_from_origin)

    def sum_attrib(self):
        sum_pos = self.to_num_dimension([0.])
        sum_vel = self.to_num_dimension([0.])
        sum_acc = self.to_num_dimension([0.])
        sum_mass = 0.
        for obj in self.objects:
            sum_acc += obj.acc * obj.mass # must be == 0
            sum_vel += obj.vel * obj.mass
            sum_pos += obj.pos * obj.mass
            sum_mass += obj.mass

        sum_pos = sum_pos / sum_mass if sum_mass != 0. else self.to_num_dimension([0.])
        sum_vel = sum_vel / sum_mass if sum_mass != 0. else self.to_num_dimension([0.])
        sum_acc = sum_acc / sum_mass if sum_mass != 0. else self.to_num_dimension([0.])
        
        return sum_mass, sum_pos, sum_vel, sum_acc

    def collide(self, p1, p2, t):
        pos = list((p1.pos * p1.mass + p2.pos * p2.mass) / (p1.mass + p2.mass))
        vel = list((p1.vel * p1.mass + p2.vel * p2.mass) / (p1.mass + p2.mass))
        acc = list(np.array([0.] * self.num_dimension))
        mass = p1.mass + p2.mass
        self.tails.append([p1.tail_coords.copy(), p1.tail_back, len(p1.tail_coords) + p1.tail_back, p1.round_size()])
        self.tails.append([p2.tail_coords.copy(), p2.tail_back, len(p2.tail_coords) + p2.tail_back, p2.round_size()])
        p3 = Planet(pos=pos,
                    vel=vel,
                    acc=acc,
                    mass=mass,
                    num_dimension=self.num_dimension,
                    tail_back=max(len(p1.tail_coords) + p1.tail_back,
                                  len(p2.tail_coords) + p2.tail_back))
        
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

    