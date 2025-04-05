# -------------------------------------------------------------------
# Library Imports
# -------------------------------------------------------------------
import _pynovi as pn
import random

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
WIDTH, HEIGHT = 600, 400
PLAYER_SPEED = 5
PLAYER_SIZE = 30
TARGET_SIZE = 20
PLAYER_COLOR = (0, 255, 0)
TARGET_COLOR = (255, 0, 0)

# -------------------------------------------------------------------
# Global Variables
# -------------------------------------------------------------------
player = None
target = None

# -------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------
def reposition_target():
    """Move the target to a new random location."""
    target.x = random.randint(0, WIDTH - TARGET_SIZE)
    target.y = random.randint(0, HEIGHT - TARGET_SIZE)

def control():
    """Move the player using arrow keys."""
    if pn.is_key_held("left"):
        player.x -= PLAYER_SPEED
    if pn.is_key_held("right"):
        player.x += PLAYER_SPEED
    if pn.is_key_held("up"):
        player.y -= PLAYER_SPEED
    if pn.is_key_held("down"):
        player.y += PLAYER_SPEED

def check_touch():
    """If the player touches the target, move the target."""
    if player.is_touching(target):
        reposition_target()

# -------------------------------------------------------------------
# Main Program
# -------------------------------------------------------------------
player = pn.create_entity(
    x=WIDTH // 2,
    y=HEIGHT // 2,
    width=PLAYER_SIZE,
    height=PLAYER_SIZE,
    color=PLAYER_COLOR
)

target = pn.create_entity(
    x=0,
    y=0,
    width=TARGET_SIZE,
    height=TARGET_SIZE,
    color=TARGET_COLOR
)
reposition_target()

pn.on_update(control)
pn.on_update(check_touch)

game = pn.Game(WIDTH, HEIGHT)
game.start()
