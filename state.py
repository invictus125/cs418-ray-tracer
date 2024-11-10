from PIL import Image
import numpy as np


class Sphere:
    x: float
    y: float
    z: float
    r: float
    color: np.ndarray
    center: np.ndarray

    def __init__(self):
        self.color = np.array([1, 1, 1])
        self.center = None

    def set_color(self, color: list[float]):
        self.color = np.array(color)

    def get_center(self):
        if self.center is None:
            self.center = np.array([self.x, self.y, self.z])

        return self.center

class Sun:
    x: float
    y: float
    z: float
    color: np.ndarray
    location: np.ndarray
    norm_direction: np.ndarray

    def __init__(self, x: float, y: float, z: float, color: list[float]):
        self.color = np.array(color)
        self.x = x
        self.y = y
        self.z = z
        self.location = np.array([x, y, z])

    def get_location(self):
        return self.location


class State:
    out_img: Image
    out_file_name: str
    out_dim_x: int
    out_dim_y: int
    max_out_dim: int
    color: list[float]
    spheres: list[Sphere]
    suns: list[Sun]
    expose: float
    forward: np.ndarray
    up: np.ndarray
    right: np.ndarray
    eye: np.ndarray


    def __init__(self):
        self.spheres = []
        self.suns = []
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