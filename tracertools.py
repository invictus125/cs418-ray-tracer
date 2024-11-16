from state import State, Sphere, Plane, Ray
import numpy as np
from math import floor, e


def trace(state: State):
    for x in range(state.out_dim_x):
        for y in range(state.out_dim_y):
            s_for_pixel = _get_s_for_pixel(x, y, state.out_dim_y, state.out_dim_x, state.max_out_dim)
            ray_for_pixel = _get_ray_for_s(
                s_for_pixel[0],
                s_for_pixel[1],
                state.forward,
                state.right,
                state.up,
                state.eye
            )
            minimum_dist_obj = None
            minimum_t = 0
            minimum_pt = None

            objs = list(state.spheres + state.planes)
            for obj in objs:
                intersection = obj.get_intersection(ray_for_pixel)
                if intersection:
                    if not minimum_dist_obj or intersection['t'] < minimum_t:
                        minimum_t = intersection['t']
                        minimum_dist_obj = obj
                        minimum_pt = intersection['pt']

            if minimum_dist_obj:
                _get_lighting_for_pixel(state, minimum_dist_obj, minimum_pt, x, y)


def _transform_srgb(value: float):
    if value > 0.0031308:
        return (1.055 * (value ** (1/2.4))) - 0.055
    else:
        return 12.92 * value


def _get_color(color: np.ndarray, expose: float):
    r = color[0]
    g = color[1]
    b = color[2]

    if expose:
        r = 1 - e ** (-expose * r)
        g = 1 - e ** (-expose * g)
        b = 1 - e ** (-expose * b)

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

    r = _transform_srgb(r)
    g = _transform_srgb(g)
    b = _transform_srgb(b)

    final_color = (
        floor(r * 255),
        floor(g * 255),
        floor(b * 255),
        255
    )

    return final_color


def _get_lighting_for_pixel(state: State, obj: Sphere | Plane, point: np.ndarray, x: int, y: int):
    color = [0, 0, 0]
    normal = obj.get_normal_at(point)
    normal = normal / np.linalg.norm(normal)

    for light in state.lights:
        light_location = light.get_location()

        light_intensity_modification = 1.0
        dist_to_bulb = -1.0
        if light.is_bulb:
            light_ray = np.subtract(light_location, point)
            dist_to_bulb = np.linalg.norm(light_ray)
            light_direction = light_ray / dist_to_bulb
            light_intensity_modification = 1 / (dist_to_bulb ** 2)
        else:
            light_direction = light_location / np.linalg.norm(light_location)

        # Factor in occlusion
        occluded = False
        ray_to_light = Ray(point, light_direction)
        
        objs = list(state.spheres + state.planes)
        for obj in objs:
            intersection = obj.get_intersection(ray_to_light)

            if intersection:
                if intersection['t'] < 1e-10:
                    # Sphere is occluding itself.
                    continue

                if light.is_bulb:
                    if intersection['t'] < dist_to_bulb:
                        occluded = True
                else:
                    # If we're not handling a bulb then it doesn't matter where the obstruction is.
                    occluded = True

        if occluded:
            continue

        lambert = np.dot(normal, light_direction) * light_intensity_modification
        if lambert < 0:
            lambert = 0

        new_color = np.multiply(
            obj.color,
            np.multiply(
                light.color,
                lambert
            )
        )
        color = np.add(
            color,
            new_color
        )

    state.out_img.im.putpixel((x, y), _get_color(color, state.expose))


def _get_s_for_pixel(x, y, h, w, max_hw):
    s_x = (2*x - w) / max_hw
    s_y = (h - 2*y) / max_hw
    return [s_x, s_y]


def _get_ray_for_s(s_x, s_y, fwd_v, right_v, up_v, eye):
    dir = np.add(np.add(fwd_v, np.multiply(s_x, right_v)), np.multiply(s_y, up_v))

    return Ray(eye, dir)
