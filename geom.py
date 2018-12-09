#!/usr/bin/env python3

'''TODO Information
For more information see:
www.github.com/zotho

'''

__author__ = "Sviatoslav Alexeev"
__email__ = "svjatoslavalekseef2@gmail.com"
__status__ = "Developed"


import numpy as np


'''TODO

Shape               _coord_dict
    Point           coord_array                     
    Poly            point_array
        Line            point_array
    Geom            poly_array point_array
        Projection      poly_array point_array
'''


class Shape():
    '''Shape([ n_dimensions:int>0 ])

    '''
    name = "shape"
    # for future (can add new coordinate)
    _coord_dict = {'x': 0, 'y': 1, 'z': 2}

    def __init__(self, *args, **kwargs):
        # Shape(n_dimensions)
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
    '''Point([ x, ... ])

    '''
    name = "point"

    def __init__(self, *args, **kwargs):
        # Point(x, ...)
        if not kwargs and len(args) == 1 and isinstance(args[0], (list, tuple)):
            if len(args[0]) <= len(self._coord_dict):
                coords = list(args[0])
                coords += [0.] * (len(self._coord_dict) - len(coords))
                self.coord_array = np.array(coords)
        # Point()
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
        if index in self._coord_dict:
            return self.coord_array[self._coord_dict.get(index)]
        else:
            self._error((index), None, name=self.name, err_name="Bad coordinate name")

    # p.x = x
    def __setattr__(self, index, value):
        if index in self._coord_dict:
            if isinstance(value, (int, float)):
                self.coord_array[self._coord_dict.get(index)] = value
            else:
                self._error((index), None, name=self.name, err_name="Bad value")
        else:
            self.__dict__[index] = value

class Poly(Shape):
    '''Poly([ [point0, ...], [[n_start, n_end], ...] ])
    Poly()

    '''
    name = "poly"

    def __init__(self, *args, **kwargs):
        # Poly([point0, ...], [[n_start, n_end], ...])
        if not kwargs and len(args) == 2 and \
                isinstance(args[0], (list, tuple)) and isinstance(args[1], (list, tuple)):
            points, pairs = args
            # check points
            for point in points:
                if not isinstance(point, Point):
                    return self._error(args, kwargs, name=self.name, err_name="Bad argument expected point")
            for l_point in range(len(points)):
                for r_point in range(l_point + 1, len(points)):
                    if points[l_point] is points[r_point]:
                        return self._error(args, kwargs, name=self.name, err_name="Bad argument points repeated")
            # check pairs
            for pair in pairs:
                if not isinstance(pair, (list, tuple)) or not len(pair) == 2 or \
                        not isinstance(pair[0], int) or pair[0] >= len(points) or pair[0] < 0 or \
                        not isinstance(pair[1], int) or pair[1] >= len(points) or pair[1] < 0 or \
                        pair[0] == pair[1]:
                    return self._error(args, kwargs, name=self.name, err_name="Bad argument expected pairs")
            for l_pair in range(len(pairs)):
                for r_pair in range(l_pair + 1, len(pairs)):
                    print(f'l_pair{l_pair}r_pair{r_pair}')
                    if pairs[l_pair] == pairs[r_pair] or pairs[l_pair][::-1] == pairs[r_pair]:
                        return self._error(args, kwargs, name=self.name, err_name="Bad argument pairs repeated or has reverse pair")

            self.point_array = np.array([point.coord_array for point in points])
            self.pair_array = np.array(pairs)
        # Poly()
        elif not args and not kwargs:
            self.point_array = np.array([])
            self.pair_array = np.array([])
        else:
            self._error(args, kwargs, name=self.name, err_name="Bad arguments")


    def add_point(self, *args, **kwargs):
        '''add_point(point [ , from=start_point ])

        '''
        pass

    def add_line(self, *args, **kwargs):
        '''add_line(n_start, n_end)
        add_line(point_start, point_end)
        add_line(array_start, array_end)

        '''
        pass

    '''
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
    '''


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
    p1 = Point([1,2,3])
    p2 = Point([4,5,6])
    pol = Poly([p,p1,p2],[[0,2],[1,2]])
    print(pol.point_array)
    print(pol.pair_array)