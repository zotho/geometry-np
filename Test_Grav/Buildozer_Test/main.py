#!/usr/bin/env python3

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window

from numpy import array2string

from functools import partial

from space import Space
from fps import Fps
from lineprinter import LinePrinter

class GravApp(App):
    def __init__(self, *args, **kwargs):
        super(GravApp, self).__init__(*args, **kwargs)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # work aroung bug [1]
        self.y = 0

        self.printer = LinePrinter('[{level:<7}] '
                                   '[{sublevel:<12}] '
                                   '[{fps:>5.2f} fps] '
                                   '[{speed:>4.1f}x speed] '
                                   'mass={mass} '
                                   'pos={pos} '
                                   'vel={vel} '
                                   'acc={acc}',
                                   level='INFO',
                                   sublevel='Log',
                                   fps=1.,
                                   speed=1.,
                                   mass=0.,
                                   pos=0.,
                                   vel=0.,
                                   acc=0.)

        self.nparray2string = partial(array2string,
                                      separator=',',
                                      formatter={'float_kind':lambda x: f"{x:6.2f}"})

    # work aroung bug [1] https://github.com/kivy/kivy/issues/5359
    def to_window(self, x, y, initial=True, relative=False):
        return x, y

    def build(self, *args, **kwargs):
        self.draw_fps = True
        self.fps = Fps()

        self.time = 0.
        self.last_time = 0.
        self.time_mult = 1.

        Clock.schedule_interval(self.update, 0)

        self.root = Space()
        return self.root

    def update(self, dt):
        # self.dt = dt
        self.time += dt * self.time_mult

        if abs(self.time - self.last_time) >= abs(self.time_mult):
            self.last_time = self.time
            mass, pos, vel, acc = self.root.sum_attrib()
            self.printer._print(fps=Clock.get_fps(),
                                mass=mass,
                                pos=self.nparray2string(pos),
                                vel=self.nparray2string(vel),
                                acc=self.nparray2string(acc))

        self.root.update(dt * self.time_mult, self.time)

        if self.draw_fps:
            self.fps.update(dt)
            self.fps.draw(self.root)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print(keycode)
        if 'd' in keycode or 100 in keycode:
            self.root.show_acc = not self.root.show_acc
            self.root.show_vel = not self.root.show_vel
            sublevels = ('Log', 'Debug')
            self.printer._print(sublevel=sublevels[self.root.show_acc])
        if 'escape' in keycode or 27 in keycode or \
                'q' in keycode or 113 in keycode:
            del self.printer
            App.get_running_app().stop()
        if 'left' in keycode or 276 in keycode:
            self.time_mult -= 0.1
            self.printer._print(speed=self.time_mult)
        if 'right' in keycode or 275 in keycode:
            self.time_mult += 0.1
            self.printer._print(speed=self.time_mult)
        if 'down' in keycode or 274 in keycode:
            self.root.set_vel([0.])
            _, _, vel, _ = self.root.sum_attrib()
            self.printer._print(vel=self.nparray2string(vel))
        return False

if __name__ == "__main__":
    GravApp().run()