#!/usr/bin/env python3
# -*- coding: utf-8
'''
    TODO Information
    For more information see:
    www.github.com/zotho
'''

__author__ = "Sviatoslav Alexeev"
__email__ = "svjatoslavalekseef2@gmail.com"
__status__ = "Developed"


import numpy as np


'''
TODO

Shape               _coord_dict
    Point           coord_array                     
    Poly            point_array
        Line            point_array
    Geom            poly_array point_array
        Projection      poly_array point_array
'''


class Shape():
    '''Shape([n_dimensions:int>0])

    '''
    name = "shape"
    # for future (can add new coordinate)
    _coord_dict = {'x': 0, 'y': 1, 'z': 2}

    def __init__(self, *args, **kwargs):
        # Shape(n)
        if not kwargs and len(args) == 1 and isinstance(args[0], int):
            new_len = args[0]
            if new_len > len(self._coord_dict):
                # TODO
                # add more coordinates
                self._error(args, kwargs, name=self.name, err_name="Can't add dimension (try <= 3)")
            elif new_len > 0:
                self._coord_dict = {key:index for key,index in self._coord_dict.items() if index < new_len}
            elif new_len <= 0:
                self._error(args, kwargs, name=self.name, err_name="Numder of dimensions can't be zero or negative")
        # Shape()
        elif not args and not kwargs:
            pass
        else:
            self._error(args, kwargs, name=self.name, err_name="Bad arguments")

    def get_dimension_dict(self):
        '''Return dictionary represent dimensions of shape
        default is {'x': 0, 'y': 1, 'z': 2}

        '''
        return self._coord_dict.copy()

    def _error(self, *args, **kwargs):
        '''Raise exception.
        _error(args, kwargs, name=self.name, err_name="...")
        
        '''
        if len(args) == 2 and len(kwargs) == 2 and \
            "name" in kwargs and "err_name" in kwargs:
            err_type = TypeError
            err_str = f"in '{kwargs.get('name')}' class - '{kwargs.get('err_name')}':\n"\
                      f"{' '*(len(err_type.__name__)+2)}{args[0]}, {args[1]}"
            raise err_type(err_str)
        else:
            raise Exception(f"Bad arguments for error: {args}, {kwargs}")

    def __str__(self):
        out = f"{self.name}:"
        out += f"\n{' '*len(out)}{self._coord_dict}"
        return out


class Point(Shape):
    '''Point([x, [y, z]])

    '''
    name = "point"

    def __init__(self, *args, **kwargs):
        # Point(x, [y, z])
        if not kwargs and len(args) == 1 and isinstance(args[0], (list, tuple)):
            if len(args[0]) <= len(self._coord_dict):
                coords = list(args[0])
                coords += [0.] * (len(self._coord_dict) - len(coords))
                self.coord_array = np.array(coords)
        elif not args and not kwargs:
            coords = [0.] * len(self._coord_dict)
            self.coord_array = np.array(coords)
        else:
            self._error(args, kwargs, name=self.name, err_name="Bad arguments")

    def __str__(self):
        out = f"{self.name}{self.coord_array}"
        return out

    # x = p['x']
    def __getitem__(self, index):
        if index in self._coord_dict:
            return self.coord_array[self._coord_dict.get(index)]
        else:
            self._error((index), None, name=self.name, err_name="Bad coordinate name")

    # p['x'] = x
    def __setitem__(self, index, value):
        if index in self._coord_dict:
            if isinstance(value, (int, float)):
                self.coord_array[self._coord_dict.get(index)] = value
            else:
                self._error((index), None, name=self.name, err_name="Bad value")
        else:
            self._error((index), None, name=self.name, err_name="Bad coordinate name")

    # x = p.x
    def __getattr__(self, index):
        # print(f'__getattr__({index})')
        if index in self._coord_dict:
            return self.coord_array[self._coord_dict.get(index)]
        else:
            self._error((index), None, name=self.name, err_name="Bad coordinate name")

    # p.x = x
    def __setattr__(self, index, value):
        # print(f'__setattr__({index})')
        if index in self._coord_dict:
            if isinstance(value, (int, float)):
                self.coord_array[self._coord_dict.get(index)] = value
            else:
                self._error((index), None, name=self.name, err_name="Bad value")
        else:
            self.__dict__[index] = value

class Poly(Shape):
    '''Poly()

    '''
    name = "poly"

    def __init__():
        # self.point_array
        # Poly([point0, ...], [[n_start, n_end], ...])
        if not args and not kwargs:
            self.point_array = np.array([])
        # Poly()


    def add_point(self, *args, **kwargs):
        '''add_point(point)

        '''
        pass

    def add_line(self, *args, **kwargs):
        '''add_line(n_start, n_end)
        
        '''
        pass

    def __str__(self):
        pass

    def __getitem__(self, index):
        pass

    def __setitem__(self, index, value):
        pass

    def __getattr__(self, index):
        pass

    def __setattr__(self, index, value):
        pass


if __name__ == "__main__":
    s = Shape(2)
    print(s)
    s1 = Shape()
    print(s1)
    l = [4,3.]
    p = Point(l)
    print(p)
    p.x = 5.8
    print(p)
    print(f'p.x + p.y + p.z = {p.x + p.y + p.z}')