import _pynovi as pn
import random

ASSETS_FOLDER = "spaceinvaders"

# Game configuration
WIDTH, HEIGHT = 800, 600
INVADER_ROWS = 3
INVADER_COLS = 8
EDGE_MARGIN = 30
MOVE_STEP = 10  # Horizontal move step, must divide evenly into screen width to prevent jitter
MOVE_INTERVAL = [30]  # Frames between invader moves
LAST_MOVE_FRAME = [-1]  # Last frame invaders moved
PLAYER_SPEED = 5
BULLET_SPEED = -8
INVADER_BULLET_SPEED = 5

# Game state
player = pn.create_entity(x=375, y=550, width=50, height=20, color=(0, 255, 0))
bullet = None
invaders = []
invader_bullets = []
direction = [1]
game_state = ["running"]  # "running", "victory", "defeat"

# Load sounds
pn.load_sound("shoot", ASSETS_FOLDER + "/shoot.wav")
pn.load_sound("explode", ASSETS_FOLDER + "/explosion.wav")
pn.load_sound("invader_move", ASSETS_FOLDER + "/move.wav")

# Create invaders
for row in range(INVADER_ROWS):
    for col in range(INVADER_COLS):
        invader = pn.create_entity(x=100 + col * 60, y=50 + row * 40, width=40, height=20, color=(255, 0, 0))
        invaders.append(invader)

pn.set_key_cooldown("space", 15)

def control():
    if game_state[0] != "running":
        return

    if pn.is_key_pressed("left") and player.x > 0:
        player.x -= PLAYER_SPEED
    if pn.is_key_pressed("right") and player.x + player.width < WIDTH:
        player.x += PLAYER_SPEED

    global bullet
    if pn.is_key_pressed("space") and bullet is None:
        bullet = pn.create_entity(
            x=player.x + player.width // 2 - 2,
            y=player.y,
            width=4,
            height=10,
            color=(255, 255, 0),
            dy=BULLET_SPEED
        )
        pn.play_sound("shoot")

def move_invaders():
    if game_state[0] != "running":
        return

    alive_invaders = [invader for invader in invaders if invader.alive]
    if not alive_invaders:
        game_state[0] = "victory"
        return

    if pn._frame_count - LAST_MOVE_FRAME[0] < MOVE_INTERVAL[0]:
        return

    # Check for edge collision first
    move_down = False
    for invader in alive_invaders:
        next_x = invader.x + direction[0] * MOVE_STEP
        if (direction[0] > 0 and next_x + invader.width > WIDTH - EDGE_MARGIN) or \
           (direction[0] < 0 and next_x < EDGE_MARGIN):
            move_down = True
            break

    # Move invaders
    for invader in alive_invaders:
        if move_down:
            invader.y += MOVE_STEP
        else:
            invader.x += direction[0] * MOVE_STEP

        if invader.is_touching(player):
            game_state[0] = "defeat"

    if move_down:
        direction[0] *= -1

    LAST_MOVE_FRAME[0] = pn._frame_count
    pn.play_sound("invader_move")

    # Update move interval based on number of invaders left
    alive_count = len(alive_invaders)
    min_interval = 2
    max_interval = 30
    total = len(invaders)
    ratio = (alive_count - 1) / (total - 1) if total > 1 else 0
    MOVE_INTERVAL[0] = int(min_interval + (max_interval - min_interval) * ratio)

    # Fire randomly
    if random.randint(1, 40) == 1:
        shooter = random.choice(alive_invaders)
        new_bullet = pn.create_entity(
            x=shooter.x + shooter.width // 2 - 2,
            y=shooter.y + shooter.height,
            width=4,
            height=10,
            color=(0, 255, 255),
            dy=INVADER_BULLET_SPEED if game_state[0] == "running" else 0
        )
        invader_bullets.append(new_bullet)

def check_collisions():
    if game_state[0] != "running":
        return

    global bullet
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

    for invader_bullet in invader_bullets:
        if invader_bullet.alive and invader_bullet.is_touching(player):
            pn.play_sound("explode")
            pn.destroy(invader_bullet)
            game_state[0] = "defeat"

    invader_bullets[:] = [b for b in invader_bullets if b.alive]

def check_player_hit():
    if game_state[0] != "running":
        return

    for invader in invaders:
        if invader.alive and invader.is_touching(player):
            game_state[0] = "defeat"
            break

def show_end_message():
    if game_state[0] == "running":
        return
    pn.end_game("YOU WIN" if game_state[0] == "victory" else "GAME OVER")

pn.on_update(control)
pn.on_update(move_invaders)
pn.on_update(check_collisions)
pn.on_update(check_player_hit)
pn.on_update(show_end_message)

game = pn.Game(WIDTH, HEIGHT)
game.start()
