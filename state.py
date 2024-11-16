from PIL import Image
import numpy as np
from math import atan2, floor


class Intersection:
    point: np.ndarray
    distance: float
    normal: np.ndarray
    texcoord: np.ndarray

    def __init__(self, pt, t, normal, texcoord):
        self.point = pt
        self.distance = t
        self.normal = normal
        self.texcoord = texcoord


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
    texture: Image
    texture_x_dim: int
    texture_y_dim: int

    def __init__(self, x, y, z, r, color: np.ndarray, texture):
        self.color = np.array(color).copy()
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.center = np.array([self.x, self.y, self.z])
        self.texture = None
        if texture is not None:
            self.texture = texture.load()
            self.texture_x_dim, self.texture_y_dim = texture.size
            print(f'tx: {self.texture_x_dim} ty: {self.texture_y_dim}')


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

        pt = np.add(t * r.dir, r.origin)

        # Calculate texture coordinate (lat and long)
        texcoord = None
        normal = np.subtract(pt, self.center) / self.r
        if self.texture is not None:
            texcoord = np.array([
                floor(
                    (
                        atan2(normal[0], normal[2]) + 1.0 / 2.0
                    ) * self.texture_x_dim
                ),
                floor(
                    (
                        atan2(
                            normal[1], (
                                (normal[0] ** 2)
                                + (normal[2] ** 2)
                            ) ** 0.5
                        ) + 1.0 / 2.0
                    ) * self.texture_y_dim
                )
            ])
            print(f'Calculated tex coord: {texcoord}')

        return Intersection(pt, t, normal, texcoord)


class LightSource:
    x: float
    y: float
    z: float
    color: np.ndarray
    location: np.ndarray
    norm_direction: np.ndarray
    is_bulb: bool

    def __init__(self, x: float, y: float, z: float, color: list[float], bulb: bool):
        self.color = np.array(color).copy()
        self.x = x
        self.y = y
        self.z = z
        self.location = np.array([x, y, z])
        self.is_bulb = True if bulb else False

    def get_location(self):
        return self.location


def _get_plane_intersection(r: Ray, normal: np.ndarray, point_on_plane: np.ndarray):
    t = np.divide(
        np.dot(
            np.subtract(point_on_plane, r.origin),
            normal
        ),
        np.dot(
            r.dir,
            normal
        )
    )

    if t <= 0:
        return None
    
    pt = np.add(np.multiply(r.dir, t), r.origin)
    
    return {
        't': t,
        'pt': pt
    }


class Plane:
    a: float
    b: float
    c: float
    d: float
    normal: np.ndarray
    point_on_plane: np.ndarray
    color: np.ndarray
    texture: Image

    def __init__(self, a, b, c, d, color):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.color = np.array(color).copy()
        self.texture = None
        nml = np.array([a, b, c])
        nmlnorm = np.linalg.norm(nml)
        self.normal = nml / nmlnorm
        self.point_on_plane = (-d * nml) / nmlnorm

    def get_intersection(self, r: Ray):
        intersection = _get_plane_intersection(r, self.normal, self.point_on_plane)
        if intersection is not None:
            return Intersection(intersection['pt'], intersection['t'], self.normal, None)
        
        return None
    
    def get_normal_at(self, _point: np.ndarray):
        return self.normal


class Vertex:
    point: np.ndarray

    def __init__(self, x: float, y: float, z: float):
        self.point = np.array([x, y, z])


class Triangle:
    v1: np.ndarray
    v2: np.ndarray
    v3: np.ndarray
    normal: np.ndarray
    color: np.ndarray
    bary_vectors: list[np.ndarray]
    texture: Image

    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex, color: np.ndarray):
        self.v1 = np.array(v1.point).copy()
        self.v2 = np.array(v2.point).copy()
        self.v3 = np.array(v3.point).copy()
        self.color = np.array(color).copy()
        self.texture = None
        e1 = np.subtract(self.v1, self.v2)
        e2 = np.subtract(self.v2, self.v3)
        e3 = np.subtract(self.v3, self.v1)
        n = np.cross(e1, e2)
        self.normal = n / np.linalg.norm(n)

        # Compute internal vectors for barycentrics
        self.bary_vectors = []
        b1 = np.cross(e1, self.normal)
        b1 = b1 / np.linalg.norm(n)
        b2 = np.cross(e2, self.normal)
        b2 = b2 / np.linalg.norm(n)
        b3 = np.cross(e3, self.normal)
        b3 = b3 / np.linalg.norm(n)
        self.bary_vectors.append(b1)
        self.bary_vectors.append(b2)
        self.bary_vectors.append(b3)

    def get_normal_at(self, _point: np.ndarray):
        return self.normal
    
    def calc_barycentric_coords(self, p: np.ndarray):
        return np.array([
            np.dot(np.subtract(p, self.v1), self.bary_vectors[0]),
            np.dot(np.subtract(p, self.v2), self.bary_vectors[1]),
            np.dot(np.subtract(p, self.v3), self.bary_vectors[2]),
        ])
    
    def get_intersection(self, r: Ray):
        plane_intersection = _get_plane_intersection(r, self.normal, self.v1)

        if plane_intersection is not None:
            barycentric = self.calc_barycentric_coords(plane_intersection['pt'])

            if np.any(barycentric < 0):
                return None
            
            return Intersection(plane_intersection['pt'], plane_intersection['t'], self.normal, None)
        
        return None


class State:
    out_img: Image
    texture: Image
    out_file_name: str
    out_dim_x: int
    out_dim_y: int
    max_out_dim: int
    color: list[float]
    objects: list[Sphere | Plane | Triangle]
    spheres: list[Sphere]
    lights: list[LightSource]
    planes: list[Plane]
    vertices: list[Vertex]
    triangles: list[Triangle]
    expose: float
    forward: np.ndarray
    up: np.ndarray
    right: np.ndarray
    eye: np.ndarray


    def __init__(self):
        self.spheres = []
        self.planes = []
        self.triangles = []
        self.vertices = []
        self.objects = []
        self.lights = []
        self.color = np.array([1.0, 1.0, 1.0])
        self.expose = None
        self.texture = None
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

    def add_sphere(self, s: Sphere):
        self.spheres.append(s)
        self.objects.append(s)

    def add_plane(self, p: Plane):
        self.planes.append(p)
        self.objects.append(p)

    def add_triangle(self, t: Triangle):
        self.triangles.append(t)
        self.objects.append(t)

    def add_vertex(self, v: Vertex):
        self.vertices.append(v)

    def get_vertex(self, idx: int):
        if idx < 0:
            return self.vertices[len(self.vertices) + idx]
        
        return self.vertices[idx - 1]

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
        print(f'lights:')
        for light in self.lights:
            print(f'\tlocation: {light.location}, color: {light.color}, isBulb: {light.is_bulb}')
        print(f'spheres:')
        for sphere in self.spheres:
            print(f'\tcenter: {sphere.center}, radius: {sphere.r}, color: {sphere.color}')
        print(f'planes:')
        for plane in self.planes:
            print(f'\tnormal: {plane.normal}, color: {plane.color}')
        print('\n\n')