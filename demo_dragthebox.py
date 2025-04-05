# -------------------------------------------------------------------
# Library Imports
# -------------------------------------------------------------------
import _pynovi as pn

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
WIDTH, HEIGHT = 600, 400
BOX_SIZE = 60
BOX_COLOR = (0, 128, 255)
BOX_COLOR_OVERLAP = (0, 255, 0)
TARGET_COLOR = (0, 200, 0)
TARGET_WIDTH = 100
TARGET_HEIGHT = 100

# -------------------------------------------------------------------
# Global Variables
# -------------------------------------------------------------------
box = None
target = None
dragging = False
offset_x = 0
offset_y = 0

# -------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------
def start_drag():
    """Start dragging if mouse pressed on box."""
    global dragging, offset_x, offset_y
    if pn.is_mouse_pressed(1) and box.is_touching_mouse():
        dragging = True
        mx, my = pn.get_mouse_position()
        offset_x = mx - box.x
        offset_y = my - box.y

def update_drag():
    """Move the box with the mouse while dragging."""
    global dragging
    if dragging:
        if pn.is_mouse_held(1):
            mx, my = pn.get_mouse_position()
            box.x = mx - offset_x
            box.y = my - offset_y
        else:
            dragging = False

def update_color():
    """Change box color when overlapping target."""
    if box.is_touching(target):
        box.color = BOX_COLOR_OVERLAP
    else:
        box.color = BOX_COLOR

# -------------------------------------------------------------------
# Main Program
# -------------------------------------------------------------------
box = pn.create_entity(
    x=50,
    y=50,
    width=BOX_SIZE,
    height=BOX_SIZE,
    color=BOX_COLOR
)

target = pn.create_entity(
    x=400,
    y=200,
    width=TARGET_WIDTH,
    height=TARGET_HEIGHT,
    color=TARGET_COLOR
)

pn.on_update(start_drag)
pn.on_update(update_drag)
pn.on_update(update_color)

game = pn.Game(WIDTH, HEIGHT)
game.start()
