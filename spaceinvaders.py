import _pynovi as pn
import random

ASSETS_FOLDER = "spaceinvaders"

WIDTH, HEIGHT = 800, 600
INVADER_ROWS = 3
INVADER_COLS = 8

player = pn.create_entity(x=375, y=550, width=50, height=20, color=(0, 255, 0))
bullet = None
invaders = []
invader_bullets = []
direction = [1]
initial_speed = 1.5
max_speed = 5
invader_speed = [initial_speed]
edge_margin = 30

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
        player.x -= 5
    if pn.is_key_pressed("right") and player.x + player.width < WIDTH:
        player.x += 5

    global bullet
    if pn.is_key_pressed("space") and bullet is None:
        bullet = pn.create_entity(
            x=player.x + player.width // 2 - 2,
            y=player.y,
            width=4,
            height=10,
            color=(255, 255, 0),
            dy=-8
        )
        pn.play_sound("shoot")

def move_invaders():
    if game_state[0] != "running":
        return

    alive_invaders = [invader for invader in invaders if invader.alive]
    if not alive_invaders:
        game_state[0] = "victory"
        return

    move_down = False
    for invader in alive_invaders:
        invader.x += direction[0] * invader_speed[0]
        if invader.is_touching(player):
            game_state[0] = "defeat"
        if (direction[0] > 0 and invader.x + invader.width >= WIDTH - edge_margin) or \
           (direction[0] < 0 and invader.x <= edge_margin):
            move_down = True

    if move_down:
        direction[0] *= -1
        # Update speed: % destroyed
        destroyed = len([i for i in invaders if not i.alive])
        total = len(invaders)
        proportion = destroyed / total
        invader_speed[0] = initial_speed + (max_speed - initial_speed) * proportion
        invader_speed[0] = min(invader_speed[0], max_speed)

        for invader in alive_invaders:
            invader.y += 10

        pn.play_sound("invader_move")

    # Invader fires randomly
    if random.randint(1, 40) == 1:
        shooter = random.choice(alive_invaders)
        new_bullet = pn.create_entity(
            x=shooter.x + shooter.width // 2 - 2,
            y=shooter.y + shooter.height,
            width=4,
            height=10,
            color=(0, 255, 255),
            dy=5 if game_state[0] == "running" else 0
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
