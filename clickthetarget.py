# -------------------------------------------------------------------
# Library Imports
# -------------------------------------------------------------------
import _pynovi as pn
import random

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
WIDTH, HEIGHT = 600, 400
TARGET_SIZE = 30
TARGET_COLOR = (255, 0, 0)
FONT_SIZE = 36

# -------------------------------------------------------------------
# Global Variables
# -------------------------------------------------------------------
target = None
score = 0

# -------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------
def reposition_target():
    """Move the target to a new random position."""
    target.x = random.randint(0, WIDTH - TARGET_SIZE)
    target.y = random.randint(0, HEIGHT - TARGET_SIZE)

def check_click():
    """If mouse clicks the target, increase score and reposition."""
    global score
    if pn.is_mouse_pressed(1) and target.is_touching_mouse():
        score += 1
        reposition_target()

def show_score():
    """Display the score at the top left."""
    pn.draw_text(f"Score: {score}", 10, 10, size=FONT_SIZE, color=(255, 255, 255))

# -------------------------------------------------------------------
# Main Program
# -------------------------------------------------------------------
target = pn.create_entity(
    x=0,
    y=0,
    width=TARGET_SIZE,
    height=TARGET_SIZE,
    color=TARGET_COLOR
)
reposition_target()

pn.on_update(check_click)
pn.on_update(show_score)

game = pn.Game(WIDTH, HEIGHT)
game.start()
