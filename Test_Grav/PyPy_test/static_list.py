#!/usr/bin/env python3

class static_list():
    def __init__(self, iterable=None, length=None, dtype=float):
        if not iterable and length:
            self.st_list = [dtype() for _ in range(length + 1)]
            self.start = 0
            self.end = 0
        elif iterable and not length:
            self.st_list = [i for i in iterable]
            self.start = 0
            self.end = len(self.st_list)
        else:
            raise AttributeError

    def append(self, obj):
        len_data = len(self.st_list)
        start = self.start
        end = self.end

        end += 1
        if end == len_data:
            end = 0

        self.st_list[end] = obj
        
        if end == start:
            start += 1
        if start == len_data:
            start = 0

        self.start = start
        self.end = end

    def _real_index(self, index):
        len_data = len(self.st_list)

        if index < self.__len__():
            real_index = self.start + index
            if real_index >= len_data:
                real_index -= len_data
            return real_index
        else:
            raise IndexError 

    def __getitem__(self, index):
        return self.st_list[self._real_index(index)]

    def __setitem__(self, index, value):
        self.st_list[self._real_index(index)] = value 

    def __len__(self):
        end = self.end
        start = self.start
        if end - start < 0:
            end += len(self.st_list)
        return end - start

if __name__ == '__main__':
    import timeit

    from collections import deque
    '''
    print(f'sl = st_list(len=10)')
    sl = static_list(length=10)

    print(f'sl.append({6})')
    sl.append(6)

    print(f'sl.append({60})')
    sl.append(60)

    for i in range(500000, 0, -2):
        print(f'sl.append({i})')
        sl.append(i)

    l = [0 for _ in range(10)]
    for i in range(500000, 0, -2):
        print(f'l.append({i})')
        l.append(i)
        l = l[-10:]

    print(f'len(sl) == {len(sl)}')

    for i in range(len(sl)):
        print(f'sl[{i}] == {sl[i]}')

    for i in range(len(l)):
        print(f'l[{i}] == {l[i]}')
    '''

    length = 10000
    range_len = 500
    numder = 200

    st0 = f'''for i in range({range_len}, 0, -2):
    sl.append(0.0 + i)'''

    st1 = f'''for i in range({range_len}, 0, -2):
    l.append(0.0 + i)
    l = l[-{length}:]'''

    st2 = f'''for i in range({range_len}, 0, -2):
    d.append(0.0 + i)'''

    print(timeit.timeit(st0,
                        setup=f'from __main__ import static_list;\
                                sl = static_list(length={length})',
                        number=numder))

    print(timeit.timeit(st1,
                        setup=f'l = [0 for _ in range({length})]',
                        number=numder))

    print(timeit.timeit(st2,
                        setup=f'from collections import deque;\
                                d = deque([0 for _ in range({length})], {length})',
                        number=numder))