import re
from PIL import Image
from state import State, Sphere, Sun
import numpy as np


###########################
# Regexes
###########################
EMPTY_LINE = re.compile("^\s*$")
COMMENT_LINE = re.compile("^#")
PNG_LINE = re.compile("^png\s")
SPHERE_LINE = re.compile("^sphere\s")
SUN_LINE = re.compile("^sun\s")
COLOR_LINE = re.compile("^color\s")


###########################
# Helpers
###########################
def should_run(line: str) -> bool:
    if EMPTY_LINE.match(line):
        return False

    if COMMENT_LINE.match(line):
        return False

    return True


def write_image(state: State):
    filename = state.out_file_name
    state.out_img.save(filename)
    print(f'Wrote {filename}')


def get_handler(line: str):
    if PNG_LINE.match(line):
        return handle_png
    if SPHERE_LINE.match(line):
        return handle_sphere
    if SUN_LINE.match(line):
        return handle_sun
    if COLOR_LINE.match(line):
        return handle_color
    else:
        print(f'Unhandled command: {line}\n')
        return None
    

###########################
# Command handlers
###########################
def handle_png(line: str, state: State):
    parts = line.split()

    if len(parts) < 4:
        raise ValueError(f'Invalid PNG line: {line}\n')
    
    state.out_dim_x = int(parts[1])
    state.out_dim_y = int(parts[2])
    state.max_out_dim = max(state.out_dim_x, state.out_dim_y)
    state.out_file_name = parts[3]
    state.out_img = Image.new("RGBA", (state.out_dim_x, state.out_dim_y), (0,0,0,0))


def handle_sphere(line: str, state: State):
    parts = line.split()

    if len(parts) < 5:
        raise ValueError(f'Invalid sphere line: {line}\n')
    
    new_sphere = Sphere()
    new_sphere.x = float(parts[1])
    new_sphere.y = float(parts[2])
    new_sphere.z = float(parts[3])
    new_sphere.r = float(parts[4])

    new_sphere.set_color(state.color)

    state.spheres.append(new_sphere)


def handle_sun(line: str, state: State):
    parts = line.split()

    if len(parts) < 4:
        raise ValueError(f'Invalid sun line: {line}\n')
    
    new_sun = Sun(float(parts[1]), float(parts[2]), float(parts[3]), state.color)

    state.suns.append(new_sun)


def handle_color(line: str, state: State):
    parts = line.split()

    if len(parts) < 4:
        raise ValueError(f'Invalid color line: {line}\n')
    
    state.color = np.array([float(parts[1]), float(parts[2]), float(parts[3])])

