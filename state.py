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

    def __init__(self):
        self.spheres = []
        self.suns = []
        self.color = np.array([1.0, 1.0, 1.0])