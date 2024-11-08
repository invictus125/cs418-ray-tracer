from state import State, Sphere, Sun
import numpy as np


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
                _get_lighting_for_pixel(state, minimum_dist_sphere, minimum_pt, x, y)


def _get_lighting_for_pixel(state: State, sphere: Sphere, point: np.ndarray, x: int, y: int):
    color = (0, 0, 0, 255)
    state.out_img.im.putpixel((x, y), color)


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
