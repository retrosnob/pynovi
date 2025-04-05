# -------------------------------------------------------------------
# Library Imports
# -------------------------------------------------------------------
import _pynovi as pn
import random

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
WIDTH, HEIGHT = 600, 400
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 20
PLAYER_COLOR = (0, 255, 0)
PLAYER_SPEED = 5

BLOCK_WIDTH = 30
BLOCK_HEIGHT = 30
BLOCK_COLOR = (255, 0, 0)
BLOCK_SPEED = 4
SPAWN_RATE = 30  # frames between block spawns

# -------------------------------------------------------------------
# Global Variables
# -------------------------------------------------------------------
player = None
blocks = []
frame_counter = 0
game_running = True

# -------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------
def control():
    """Move the player left and right."""
    if not game_running:
        return
    if pn.is_key_held("left") and player.x > 0:
        player.x -= PLAYER_SPEED
    if pn.is_key_held("right") and player.x + player.width < WIDTH:
        player.x += PLAYER_SPEED

def spawn_block():
    """Create a new falling block at a random x-position."""
    x = random.randint(0, WIDTH - BLOCK_WIDTH)
    block = pn.create_entity(
        x=x, y=0,
        width=BLOCK_WIDTH, height=BLOCK_HEIGHT,
        color=BLOCK_COLOR,
        dy=BLOCK_SPEED
    )
    blocks.append(block)

def update_blocks():
    """Remove off-screen blocks and check for collisions."""
    global game_running
    if not game_running:
        return

    for block in blocks:
        if block.alive and block.is_touching(player):
            game_running = False
            pn.end_game("GAME OVER")
            break

    # Remove any dead blocks
    blocks[:] = [b for b in blocks if b.alive]

def spawn_logic():
    """Spawn new blocks at fixed intervals."""
    global frame_counter
    frame_counter += 1
    if frame_counter % SPAWN_RATE == 0:
        spawn_block()

# -------------------------------------------------------------------
# Main Program
# -------------------------------------------------------------------
player = pn.create_entity(
    x=WIDTH // 2,
    y=HEIGHT - PLAYER_HEIGHT - 10,
    width=PLAYER_WIDTH,
    height=PLAYER_HEIGHT,
    color=PLAYER_COLOR
)

pn.on_update(control)
pn.on_update(spawn_logic)
pn.on_update(update_blocks)

game = pn.Game(WIDTH, HEIGHT)
game.start()
