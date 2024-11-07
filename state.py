from PIL import Image


class Sphere:
    x: float
    y: float
    z: float
    r: float
    color: list[float]

    def __init__(self):
        self.color = [1, 1, 1]

    def set_color(self, color: list[float]):
        self.color = color.copy()


class Sun:
    x: float
    y: float
    z: float
    color: list[float]

    def __init__(self):
        self.color = [1, 1, 1]

    def set_color(self, color: list[float]):
        self.color = color.copy()


class State:
    out_img: Image
    out_file_name: str
    out_dim_x: int
    out_dim_y: int
    color: list[float]
    spheres: list[Sphere]
    suns: list[Sun]

    def __init__(self):
        self.spheres = []
        self.suns = []
        self.color = [1, 1, 1]