import re
from PIL import Image
from state import State, Sphere, LightSource, Plane
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
EXPOSE_LINE = re.compile("^expose\s")
FORWARD_LINE = re.compile("^forward\s")
UP_LINE = re.compile("^up\s")
EYE_LINE = re.compile("^eye\s")
BULB_LINE = re.compile("^bulb\s")
PLANE_LINE = re.compile("^plane\s")


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
    if EXPOSE_LINE.match(line):
        return handle_expose
    if FORWARD_LINE.match(line):
        return handle_forward
    if UP_LINE.match(line):
        return handle_up
    if EYE_LINE.match(line):
        return handle_eye
    if BULB_LINE.match(line):
        return handle_bulb
    if PLANE_LINE.match(line):
        return handle_plane
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
    
    new_sphere = Sphere(float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]), state.color)

    state.add_sphere(new_sphere)


def handle_sun(line: str, state: State):
    parts = line.split()

    if len(parts) < 4:
        raise ValueError(f'Invalid sun line: {line}\n')
    
    new_sun = LightSource(float(parts[1]), float(parts[2]), float(parts[3]), state.color, False)

    state.lights.append(new_sun)


def handle_color(line: str, state: State):
    parts = line.split()

    if len(parts) < 4:
        raise ValueError(f'Invalid color line: {line}\n')
    
    state.color = np.array([float(parts[1]), float(parts[2]), float(parts[3])])


def handle_expose(line: str, state: State):
    parts = line.split()

    state.expose = float(parts[1])


def handle_forward(line: str, state: State):
    parts = line.split()

    state.set_forward([float(parts[1]), float(parts[2]), float(parts[3])])


def handle_up(line: str, state: State):
    parts = line.split()

    state.set_up([float(parts[1]), float(parts[2]), float(parts[3])])


def handle_eye(line: str, state: State):
    parts = line.split()

    state.set_eye([float(parts[1]), float(parts[2]), float(parts[3])])


def handle_bulb(line: str, state: State):
    parts = line.split()

    if len(parts) < 4:
        raise ValueError(f'Invalid sun line: {line}\n')
    
    new_bulb = LightSource(float(parts[1]), float(parts[2]), float(parts[3]), state.color, True)

    state.lights.append(new_bulb)


def handle_plane(line: str, state: State):
    parts = line.split()

    if len(parts) < 5:
        raise ValueError(f'Invalid sphere line: {line}\n')
    
    new_plane = Plane(float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]), state.color)

    state.add_plane(new_plane)
