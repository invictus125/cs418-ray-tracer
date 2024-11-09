from state import State, Sphere
import numpy as np
from math import floor


class Ray:
    dir: list[float]
    dir_mag: float
    origin: list[float]

    def __init__(self, origin, direction):
        self.origin = np.array(origin)
        self.dir = np.array(direction) / np.linalg.norm(direction)
        self.dir_mag = 1.0


def trace(state: State):
    fwd_vec = np.array([0, 0, -1])
    right_vec = np.array([1, 0, 0])
    up_vec = np.array([0, 1, 0])
    eye = np.array([0, 0, 0])
    for x in range(state.out_dim_x):
        for y in range(state.out_dim_y):
            s_for_pixel = _get_s_for_pixel(x, y, state.out_dim_y, state.out_dim_x, state.max_out_dim)
            ray_for_pixel = _get_ray_for_s(s_for_pixel[0], s_for_pixel[1], fwd_vec, right_vec, up_vec, eye)
            minimum_dist_sphere = None
            minimum_t = 0
            minimum_pt = None
            for sphere in state.spheres:
                intersection = _get_sphere_intersection(ray_for_pixel, sphere)
                if intersection:
                    if not minimum_dist_sphere or intersection['t'] < minimum_t:
                        minimum_t = intersection['t']
                        minimum_dist_sphere = sphere
                        minimum_pt = intersection['pt']

            if minimum_dist_sphere:
                _get_lighting_for_pixel(state, minimum_dist_sphere, minimum_pt, eye, x, y)


def _transform_srgb(value: float):
    if value > 0.0031308:
        return ((1.055 * value) ** (1/2.4)) - 0.055
    else:
        return 12.92 * value


def _get_color(color: np.ndarray, log: bool):
    r = _transform_srgb(color[0])
    g = _transform_srgb(color[1])
    b = _transform_srgb(color[2])

    if r < 0:
        r = 0
    elif r > 1:
        r = 1.0

    if g < 0:
        g = 0
    elif g > 1:
        g = 1.0

    if b < 0:
        b = 0
    elif b > 1:
        b = 1.0

    final_color = (
        floor(r * 255),
        floor(g * 255),
        floor(b * 255),
        255
    )

    if log:
        print(f'final color: {final_color}')

    return final_color


def _get_lighting_for_pixel(state: State, sphere: Sphere, point: np.ndarray, eye: np.ndarray, x: int, y: int):
    color = [0, 0, 0]
    normal = np.subtract(point, sphere.center)
    normal = normal / np.linalg.norm(normal)

    # log = False
    # if x == 82 and y == 70:
    #     log = True
    #     print(f'intersection point: {point}')
    #     print(f'normal: {normal}')


    for sun in state.suns:
        sun_location = sun.get_location()
        raw_sun_direction = np.subtract(sun_location, eye)
        sun_direction = raw_sun_direction / np.linalg.norm(raw_sun_direction)

        # Factor in occlusion
        occluded = False
        sun_dir_from_origin = np.subtract(sun_location, point)
        ray_to_sun = Ray(point, sun_dir_from_origin)
        for s in state.spheres:
            intersection = _get_sphere_intersection(ray_to_sun, s)

            if intersection:
                if intersection['t'] < 1e-10:
                    # Sphere is occluding itself.
                    continue

                dist_to_sun = np.linalg.norm(sun_dir_from_origin)
                if intersection['t'] < dist_to_sun:
                    print(f'sphere location: {s.get_center()}')
                    print(f'distance to sun: {dist_to_sun}')
                    print(f'intersection: {intersection}')
                    occluded = True

        if occluded:
            continue

        lambert = np.dot(normal, sun_direction)
        color = np.add(
            color,
            np.multiply(
                sphere.color,
                np.multiply(
                    sun.color,
                    lambert
                )
            )
        )
        
        # if log:
        #     print(f'lambert: {lambert}')
        #     print(f'raw sun direction: {raw_sun_direction}')
        #     print(f'sun direction: {sun_direction}')
        #     print(f'linear color: {color}')

    state.out_img.im.putpixel((x, y), _get_color(color, False))


def _get_s_for_pixel(x, y, h, w, max_hw):
    s_x = (2*x - w) / max_hw
    s_y = (h - 2*y) / max_hw
    return [s_x, s_y]


def _get_ray_for_s(s_x, s_y, fwd_v, right_v, up_v, eye):
    # direction = fwd_v + s_x * right_v + s_y * up_v
    dir = np.add(np.add(fwd_v, np.multiply(s_x, right_v)), np.multiply(s_y, up_v))

    return Ray(eye, dir)


def _get_sphere_intersection(r: Ray, s: Sphere):
    c = s.get_center()
    diff = np.subtract(c, r.origin)
    r_sqrd = s.r ** 2
    inside = ((np.linalg.norm(diff) ** 2) < r_sqrd)

    t_c = np.divide(np.dot(diff, r.dir), r.dir_mag)

    if not inside and t_c < 0:
        # No intersection
        return None
    
    d_sqrd = np.linalg.norm(np.subtract(np.add(r.origin, np.multiply(t_c, r.dir)), c)) ** 2

    if not inside and r_sqrd < d_sqrd:
        # No intersection
        return None
    
    t_offs = ((r_sqrd - d_sqrd) ** 0.5) / r.dir_mag

    if inside:
        t = t_c + t_offs
    else:
        t = t_c - t_offs

    return {
        't': t,
        'pt': np.add(t * r.dir, r.origin)
    }
