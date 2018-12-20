#!/usr/bin/env python2

from kivy.app import App                # main app
from kivy.clock import Clock            # for event loop
from kivy.core.window import Window

from space import Space                 # Space class
from fps import Fps                     # Fps meter

class GravApp(App):

    def build(self):

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

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
            print Clock.get_fps()

        self.root.update(dt * self.time_mult, self.time)

        if self.draw_fps:
            self.fps.update(dt)
            self.fps.draw(self.root)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print keycode
        if keycode[1] == 'd' or keycode[0] == 100:
            self.root.show_acc = not self.root.show_acc
            self.root.show_vel = not self.root.show_vel
        if keycode[1] == 'escape' or keycode[0] == 27 or \
                keycode[1] == 'q' or keycode[0] == 113:
            App.get_running_app().stop()
        if keycode[1] == 'left' or keycode[0] == 276:
            self.time_mult -= 0.1
            print('{:.1f} mult'.format(self.time_mult))
        if keycode[1] == 'right' or keycode[0] == 275:
            self.time_mult += 0.1
            print('{:.1f} mult'.format(self.time_mult))
        if keycode[1] == 'down' or keycode[0] == 274:
            self.root.set_vel([0.])
        return True

if __name__ == "__main__":
    GravApp().run()