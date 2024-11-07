from library import should_run, get_handler, write_image
from tracertools import trace
from state import State
import sys

master_state = State()

lines = []
with open(sys.argv[1]) as file:
    for line in file:
        line = line.strip()
        if should_run(line):
            print(line)
            handler = get_handler(line)
            if handler is not None:
                handler(line, master_state)

    file.close()

trace(master_state)

write_image(master_state)
