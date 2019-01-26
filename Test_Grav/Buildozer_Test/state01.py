
from planet import Planet


def set_state(space, app, _):
    cx, cy = space.center_x, space.center_y
    w, h = space.width, space.height

    from math import sin, cos, pi

    r = 100.
    n = 5

    for i in range(n):
        space.append(Planet(pos=(cos(i/n*2.*pi)*r+cx, sin(i/n*2.*pi)*r+cy),
                            vel=(cos(i/n*2.*pi+pi/2.)*2*r, sin(i/n*2.*pi+pi/2.)*2*r),
                            mass=0.1,
                            charge=0.1   ) )

    space.append(Planet(pos=(cx, cy),
                        vel=(0, 0),
                        mass=1.,
                        charge=-100.   ) )

    app.time_mult, app.time_mult_pause = 0., app.time_mult