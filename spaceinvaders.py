# -------------------------------------------------------------------
# Library Imports
# -------------------------------------------------------------------
import _pynovi as pn
import random

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
ASSETS_FOLDER = "spaceinvaders"
WIDTH, HEIGHT = 800, 600
INVADER_ROWS = 3
INVADER_COLS = 8
EDGE_MARGIN = 30
MOVE_STEP = 30
DROP_STEP = 30
PLAYER_SPEED = 5
BULLET_SPEED = -8
INVADER_BULLET_SPEED = 5
INVADER_WIDTH = 40
INVADER_HEIGHT = 20
INVADER_COLOR = (255, 0, 0)
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 20
PLAYER_COLOR = (0, 255, 0)
BULLET_WIDTH = 4
BULLET_HEIGHT = 10
BULLET_COLOR = (255, 255, 0)
INVADER_BULLET_COLOR = (0, 255, 255)
BULLET_COOLDOWN = 15
INVADER_START_X = 100
INVADER_START_Y = 50
INVADER_SPACING_X = 60
INVADER_SPACING_Y = 40
PLAYER_START_X = 375
PLAYER_START_Y = 550

# -------------------------------------------------------------------
# Global Variables
# -------------------------------------------------------------------
move_interval = 30
last_move_frame = -1
player = None
bullet = None
invaders = []
invader_bullets = []
direction = 1
game_state = "running"

# -------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------
def control():
    """Handle player movement and shooting."""
    # Ignore input if game is not active
    if game_state != "running":
        return

    # Move player left or right based on key input
    if pn.is_key_pressed("left") and player.x > 0:
        player.x -= PLAYER_SPEED
    if pn.is_key_pressed("right") and player.x + player.width < WIDTH:
        player.x += PLAYER_SPEED

    global bullet
    # Fire bullet if spacebar is pressed and no bullet is currently active
    if pn.is_key_pressed("space") and bullet is None:
        bullet = pn.create_entity(
            x=player.x + player.width // 2 - BULLET_WIDTH // 2,
            y=player.y,
            width=BULLET_WIDTH,
            height=BULLET_HEIGHT,
            color=BULLET_COLOR,
            dy=BULLET_SPEED
        )
        pn.play_sound("shoot")

def move_invaders():
    """Move invaders across the screen, drop them down if needed,
    adjust speed as invaders are destroyed, and randomly fire bullets."""
    global game_state, direction, last_move_frame, move_interval
    # Ignore if game is not running
    if game_state != "running":
        return

    # Get all alive invaders
    alive_invaders = [invader for invader in invaders if invader.alive]

    # If all invaders are destroyed, player wins
    if not alive_invaders:
        game_state = "victory"
        return

    # Only move invaders after enough time has passed
    if pn.Game.frame_count - last_move_frame < move_interval:
        return

    move_down = False
    # Check if any invader is about to hit the screen edge
    for invader in alive_invaders:
        next_x = invader.x + direction * MOVE_STEP
        if (
            (direction > 0 and next_x + invader.width > WIDTH - EDGE_MARGIN) or
            (direction < 0 and next_x < EDGE_MARGIN)
        ):
            move_down = True
            break

    # Move invaders horizontally or drop them down
    for invader in alive_invaders:
        if move_down:
            invader.y += DROP_STEP
        else:
            invader.x += direction * MOVE_STEP

        if invader.is_touching(player):
            game_state = "defeat"

    # Reverse direction if invaders hit the edge
    if move_down:
        direction *= -1

    # Record the last time invaders moved
    last_move_frame = pn.Game.frame_count
    pn.play_sound("invader_move")

    # Adjust move speed based on how many invaders are left
    alive_count = len(alive_invaders)
    min_interval = 2
    max_interval = 30
    total = len(invaders)
    ratio = (alive_count - 1) / (total - 1) if total > 1 else 0
    move_interval = int(min_interval + (max_interval - min_interval) * ratio)

    # Randomly fire a bullet from one of the invaders
    if random.randint(1, 40) == 1:
        shooter = random.choice(alive_invaders)
        new_bullet = pn.create_entity(
            x=shooter.x + shooter.width // 2 - BULLET_WIDTH // 2,
            y=shooter.y + shooter.height,
            width=BULLET_WIDTH,
            height=BULLET_HEIGHT,
            color=INVADER_BULLET_COLOR,
            dy=INVADER_BULLET_SPEED if game_state == "running" else 0
        )
        invader_bullets.append(new_bullet)

def check_collisions():
    """Check for collisions between bullets and invaders,
    or between invader bullets and the player."""
    global game_state
    # Exit if the game is not running
    if game_state != "running":
        return

    global bullet
    # Check if player bullet hits an invader
    if bullet:
        for invader in invaders:
            if invader.alive and bullet.is_touching(invader):
                pn.play_sound("explode")
                pn.destroy(invader)
                pn.destroy(bullet)
                bullet = None
                break
        if bullet and not bullet.alive:
            bullet = None

    # Check if any invader bullet hits the player
    for invader_bullet in invader_bullets:
        if invader_bullet.alive and invader_bullet.is_touching(player):
            pn.play_sound("explode")
            pn.destroy(invader_bullet)
            game_state = "defeat"

    # Remove any invader bullets that are no longer active
    invader_bullets[:] = [b for b in invader_bullets if b.alive]

def check_player_hit():
    """Check if any invader has reached the player directly."""
    global game_state
    # Exit if game is not active
    if game_state != "running":
        return

    for invader in invaders:
        if invader.alive and invader.is_touching(player):
            game_state = "defeat"
            break

def show_end_message():
    """Display win or lose message at the end of the game."""
    # Only show message if game has ended
    if game_state == "running":
        return
    pn.end_game("YOU WIN" if game_state == "victory" else "GAME OVER")

# -------------------------------------------------------------------
# Main Program
# -------------------------------------------------------------------
player = pn.create_entity(x=PLAYER_START_X, y=PLAYER_START_Y, width=PLAYER_WIDTH, height=PLAYER_HEIGHT, color=PLAYER_COLOR)

pn.load_sound("shoot", ASSETS_FOLDER + "/shoot.wav")
pn.load_sound("explode", ASSETS_FOLDER + "/explosion.wav")
pn.load_sound("invader_move", ASSETS_FOLDER + "/move.wav")

for row in range(INVADER_ROWS):
    for col in range(INVADER_COLS):
        invader = pn.create_entity(
            x=INVADER_START_X + col * INVADER_SPACING_X,
            y=INVADER_START_Y + row * INVADER_SPACING_Y,
            width=INVADER_WIDTH,
            height=INVADER_HEIGHT,
            color=INVADER_COLOR
        )
        invaders.append(invader)

pn.set_key_cooldown("space", BULLET_COOLDOWN)

pn.on_update(control)
pn.on_update(move_invaders)
pn.on_update(check_collisions)
pn.on_update(check_player_hit)
pn.on_update(show_end_message)

game = pn.Game(WIDTH, HEIGHT)
game.start()
