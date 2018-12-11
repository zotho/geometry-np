#!/usr/bin/env python3

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.widget import Widget

KV = '''
#:import chain itertools.chain
#:import sin math.sin
#:import cos math.cos
#:import pi math.pi
<Flower>:
    iangle: (2. * pi) / self.petals
    color: (abs(sin(app.time)) + sin(app.time))/2, \
           (abs(sin(app.time - 2. * pi / 3.)) + sin(app.time - 2. * pi / 3.))/2, \
           (abs(sin(app.time - 4. * pi / 3.)) + sin(app.time - 4. * pi / 3.))/2, \
           .1
    vertices:
        list(
        chain(*[(
        self.center_x + sin(app.time) * .8 * root.radius * cos(root.iangle * n),
        self.center_y + sin(app.time) * .8 * root.radius * sin(root.iangle * n),
        0, 0,
        self.center_x + sin(app.time) * .8 * root.radius * cos(root.iangle * n + sin(app.time)) + cos(2 * pi * a / self.precision) * root.radius,
        self.center_y + sin(app.time) * .8 * root.radius * sin(root.iangle * n + cos(app.time)) + sin(2 * pi * a / self.precision) * root.radius,
        0, 0,
        self.center_x + sin(app.time) * .8 * root.radius * cos(root.iangle * n + sin(app.time)) + cos(2 * pi * (a + 1) / self.precision) * root.radius,
        self.center_y + sin(app.time) * .8 * root.radius * sin(root.iangle * n + cos(app.time)) + sin(2 * pi * (a + 1) / self.precision) * root.radius,
        0, 0
        ) for a in range(self.precision) for n in range(root.petals)])
        )
    canvas:
        Color:
            rgba: self.color
        Mesh:
            mode: 'triangles'
            vertices: self.vertices if self.vertices else []
            indices: range(len(self.vertices) // 4) if self.vertices else []
'''  # noqa


class Flower(Widget):
    petals = NumericProperty(10)
    radius = NumericProperty(200)
    iangle = NumericProperty(0)
    precision = NumericProperty(20)
    color = ListProperty([1, 1, 1, .1])


class BnBApp(App):
    time = NumericProperty(0)

    def build(self):
        Builder.load_string(KV)
        Clock.schedule_interval(self.update_time, 0)
        self.root = Flower(petals=3, precision=10)
        return self.root

    def update_time(self, dt):
        self.time += dt


if __name__ == '__main__':
    BnBApp().run()