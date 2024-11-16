from PIL import Image
import numpy as np


class Ray:
    dir: list[float]
    dir_mag: float
    origin: list[float]

    def __init__(self, origin, direction):
        self.origin = np.array(origin)
        self.dir = np.array(direction) / np.linalg.norm(direction)
        self.dir_mag = 1.0


class Sphere:
    x: float
    y: float
    z: float
    r: float
    color: np.ndarray
    center: np.ndarray

    def __init__(self, x, y, z, r, color: np.ndarray):
        self.color = np.array(color)
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.center = np.array([self.x, self.y, self.z])

    def get_center(self):
        return self.center
    
    def get_normal_at(self, point: np.ndarray):
        return np.subtract(point, self.center)
    
    def get_intersection(self, r: Ray):
        c = self.get_center()
        diff = np.subtract(c, r.origin)
        r_sqrd = self.r ** 2
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


class LightSource:
    x: float
    y: float
    z: float
    color: np.ndarray
    location: np.ndarray
    norm_direction: np.ndarray
    is_bulb: bool

    def __init__(self, x: float, y: float, z: float, color: list[float], bulb: bool):
        self.color = np.array(color)
        self.x = x
        self.y = y
        self.z = z
        self.location = np.array([x, y, z])
        self.is_bulb = True if bulb else False

    def get_location(self):
        return self.location


class Plane:
    a: float
    b: float
    c: float
    d: float
    normal: np.ndarray
    point_on_plane: np.ndarray
    color: np.ndarray

    def __init__(self, a, b, c, d, color):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.color = np.array(color)
        nml = np.array([a, b, c])
        nmlnorm = np.linalg.norm(nml)
        self.normal = nml / nmlnorm
        self.point_on_plane = (-d * nml) / nmlnorm

    def get_intersection(self, r: Ray):
        t = np.divide(
            np.dot(
                np.subtract(self.point_on_plane, r.origin),
                self.normal
            ),
            np.dot(
                r.dir,
                self.normal
            )
        )

        if t <= 0:
            return None
        
        pt = np.add(np.multiply(r.dir, t), r.origin)
        
        return {
            't': t,
            'pt': pt
        }
    
    def get_normal_at(self, _point: np.ndarray):
        return self.normal


class State:
    out_img: Image
    out_file_name: str
    out_dim_x: int
    out_dim_y: int
    max_out_dim: int
    color: list[float]
    spheres: list[Sphere]
    lights: list[LightSource]
    planes: list[Plane]
    expose: float
    forward: np.ndarray
    up: np.ndarray
    right: np.ndarray
    eye: np.ndarray


    def __init__(self):
        self.spheres = []
        self.planes = []
        self.lights = []
        self.color = np.array([1.0, 1.0, 1.0])
        self.expose = None
        self.forward = np.array([0, 0, -1])
        self.up = np.array([0, 1, 0])
        self.eye = np.array([0, 0, 0])
        self.right = np.array([1, 0, 0])

    def set_forward(self, fwd):
        self.forward = np.array(fwd)
        self.right = np.cross(self.forward, self.up)
        self.right = self.right / np.linalg.norm(self.right)
        self.up = np.cross(self.right, self.forward)
        self.up = self.up / np.linalg.norm(self.up)
    
    def set_up(self, up):
        self.up = np.array(up)
        self.right = np.cross(self.forward, self.up)
        self.right = self.right / np.linalg.norm(self.right)
        self.up = np.cross(self.right, self.forward)
        self.up = self.up / np.linalg.norm(self.up)

    def set_eye(self, eye):
        self.eye = np.array(eye)

    def log_state(self):
        print('\n\n')
        print('CURRENT STATE:\n')
        print(f'image: {self.out_file_name} w: {self.out_dim_x} h: {self.out_dim_y}')
        print(f'color: {self.color}')
        print(f'expose: {self.expose}')
        print(f'eye location: {self.eye}')
        print(f'forward vec: {self.forward}')
        print(f'up vec: {self.up}')
        print(f'right vec: {self.right}')
        print('\n\n')