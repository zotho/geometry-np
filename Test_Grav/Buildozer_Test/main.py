#!/usr/bin/env python3

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config

from numpy import array2string, pi

from functools import partial

from space import Space
from fps import Fps
from lineprinter import LinePrinter

ANGLE = pi/18.

from kivy.core.window import Window
Window.borderless = True
Window.hide()

class GravApp(App):
    def __init__(self, *args, **kwargs):
        super(GravApp, self).__init__(*args, **kwargs)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down,
                            on_key_up=self._on_keyboard_up)
        self._keyboard_modifiers = []

        # work aroung bug [1]
        self.y = 0
        '''
                                   'mass={mass} '
                                   'pos={pos} '
                                   'vel={vel} '
                                   'acc={acc} '
        '''
        self.printer = LinePrinter('[{level:<7}] '
                                   '[{sublevel:<12}] '
                                   '[{fps:>5.2f} fps] '
                                   '[{speed:>4.1f}x speed] '
                                   'npoints=[{points}]'
                                   '{debug}',
                                   level='INFO',
                                   sublevel='Log',
                                   fps=1.,
                                   speed=1.,
                                   mass=0.,
                                   pos=0.,
                                   vel=0.,
                                   acc=0.,
                                   points=0,
                                   debug='')

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
        self.event_once = None

        self.root = Space()

        Config.read('config.ini')

        # For my window header
        # dx, dy = -1, -32
        dx, dy = 0, 0

        if Config.get('graphics', 'position') != 'auto':
            Window.left, Window.top, Window.size = Config.getint('graphics', 'left') + dx, \
                                                   Config.getint('graphics', 'top') + dy, \
                                                   (Config.getint('graphics', 'width'), \
                                                    Config.getint('graphics', 'height'),)
        if Config.getboolean('graphics', 'maximize'):
            Window.maximize()
        
        window_pref = Window.left, Window.top, Window.size
        def window_once(_):
            w_p = window_pref
            Window.left, Window.top, Window.size = w_p
        Window.show()
        #Clock.schedule_once(window_once, 2)
        
        return self.root

    def update(self, dt):
        print(f'left={Window.left}, top={Window.top}, width={Window.width}, height={Window.height}')
        # self.dt = dt
        self.time += dt * self.time_mult

        if abs(self.time - self.last_time) >= abs(self.time_mult):
            self.last_time = self.time
            mass, pos, vel, acc = self.root.sum_attrib()
            self.printer.print(fps=Clock.get_fps(),
                               mass=mass,
                               pos=self.nparray2string(pos),
                               vel=self.nparray2string(vel),
                               acc=self.nparray2string(acc),
                               points=len(self.root.objects))

        _, pos, _, _ = self.root.sum_attrib()
        # self.root.rotate(-pi/180., (0., 1., 0), (0., 0., 1.))
        self.root.rotate(dt * self.time_mult * -ANGLE, (1., 0., 0), (0., 0., 1.), pos)

        self.root.update(dt * self.time_mult, self.time)

        if self.draw_fps:
            self.fps.update(dt)
            self.fps.draw(self.root)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] in self._keyboard_modifiers:
            self._keyboard_modifiers.remove(keycode[1])
        return False

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        '''
        print(keycode)
        print(text)
        print(modifiers)
        '''

        if self.event_once:
            self.event_once.get_callback()()
            self.event_once.cancel()
        
        format_string = self.printer.format_string
        data = self.printer.data
        def to_prev(*args, **kwargs):
            self.printer.format_string = format_string
            self.printer.data = data
            self.printer.print()
        self.event_once = Clock.create_trigger(to_prev, 1)
        self.event_once()
        text = (modifiers if keycode[1] not in modifiers else []) + [keycode[1],]
        self.printer.print(format_string + ' key=[{key}]', key='+'.join(text).upper())

        self._keyboard_modifiers = modifiers

        if 'shift' in modifiers:
            if 'left' == keycode[1] or 276 == keycode[0]:
                _, pos, _, _ = self.root.sum_attrib()
                self.root.rotate(ANGLE, (1., 0., 0), (0., 0., 1.), pos)
            if 'right' == keycode[1] or 275 == keycode[0]:
                _, pos, _, _ = self.root.sum_attrib()
                self.root.rotate(ANGLE, (1., 0., 0), (0., 0., 1.), pos)
            if 'down' == keycode[1] or 274 == keycode[0]:
                _, pos, _, _ = self.root.sum_attrib()
                self.root.rotate(ANGLE, (0., 1., 0), (0., 0., 1.), pos)
            if 'up' == keycode[1] or 273 == keycode[0]:
                _, pos, _, _ = self.root.sum_attrib()
                self.root.rotate(ANGLE, (0., 1., 0), (0., 0., 1.), pos)
        elif not modifiers:
            if 'd' == keycode[1] or 100 == keycode[0]:
                self.root.show_acc = not self.root.show_acc
                self.root.show_vel = not self.root.show_vel
                sublevels = ('Log', 'Debug')
                debug_format = ' mass={mass} pos={pos} vel={vel} acc={acc}'
                self.printer.print(sublevel=sublevels[self.root.show_acc],
                                   debug=debug_format if self.root.show_acc else '')
            if 'escape' == keycode[1] or 27 == keycode[0] or \
                    'q' == keycode[1] or 113 == keycode[0]:
                del self.printer

                Config.set('graphics', 'position', 'custom')
                Config.set('graphics', 'width', Window.width)
                Config.set('graphics', 'height', Window.height)
                Config.set('graphics', 'left', Window.left)
                Config.set('graphics', 'top', Window.top)
                Config.write()

                App.get_running_app().stop()

            if 'left' == keycode[1] or 276 == keycode[0]:
                self.time_mult -= 0.1
                self.printer.print(speed=self.time_mult)
            if 'right' == keycode[1] or 275 == keycode[0]:
                self.time_mult += 0.1
                self.printer.print(speed=self.time_mult)
            if 'down' == keycode[1] or 274 == keycode[0]:
                self.root.set_vel([0.])
                _, _, vel, _ = self.root.sum_attrib()
                self.printer.print(vel=self.nparray2string(vel))
            if 'up' == keycode[1] or 273 == keycode[0]:
                self.root.set_pos(Window.center)
                _, pos, _, _ = self.root.sum_attrib()
                self.printer.print(vel=self.nparray2string(pos))
        return False

if __name__ == "__main__":
    GravApp().run()