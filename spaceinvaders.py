import _pynovi as pn
import random

ASSETS_FOLDER = "spaceinvaders"

WIDTH, HEIGHT = 800, 600
player = pn.create_entity(x=375, y=550, width=50, height=20, color=(0, 255, 0))
bullet = None
invaders = []
invader_bullets = []
direction = [1]  # 1 = right, -1 = left
invader_speed = [2]
edge_margin = 30

game_over = [False]  # Mutable flag to coordinate game state
victory = [False]    # Flag to show if the player won

# Load sounds
pn.load_sound("shoot", ASSETS_FOLDER + "/shoot.wav")
pn.load_sound("explode", ASSETS_FOLDER + "/explosion.wav")

# Create invaders
for row in range(3):
    for col in range(8):
        invader = pn.create_entity(x=100 + col * 60, y=50 + row * 40, width=40, height=20, color=(255, 0, 0))
        invaders.append(invader)

# Key cooldown
pn.set_key_cooldown("space", 15)

def control():
    if game_over[0]:
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
    if game_over[0]:
        return

    if all(not invader.alive for invader in invaders):
        victory[0] = True
        game_over[0] = True
        pn.end_game()
        return

    move_down = False
    for invader in invaders:
        if invader.alive:
            invader.x += direction[0] * invader_speed[0]
            if invader.is_touching(player):
                pn.end_game()
                game_over[0] = True
            if (direction[0] > 0 and invader.x + invader.width >= WIDTH - edge_margin) or \
               (direction[0] < 0 and invader.x <= edge_margin):
                move_down = True

    if move_down:
        direction[0] *= -1
        invader_speed[0] += 0.2
        for invader in invaders:
            if invader.alive:
                invader.y += 10

    # Random invader fires a bullet occasionally
    if random.randint(1, 40) == 1:
        shooters = [invader for invader in invaders if invader.alive]
        if shooters:
            shooter = random.choice(shooters)
            bullet = pn.create_entity(
                x=shooter.x + shooter.width // 2 - 2,
                y=shooter.y + shooter.height,
                width=4,
                height=10,
                color=(0, 255, 255),
                dy=5
            )
            invader_bullets.append(bullet)

def check_collisions():
    if game_over[0]:
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
            game_over[0] = True
            pn.end_game()

    invader_bullets[:] = [b for b in invader_bullets if b.alive]

def check_player_hit():
    if game_over[0]:
        return

    for invader in invaders:
        if invader.alive and invader.is_touching(player):
            game_over[0] = True
            pn.end_game()
            break

def show_end_message():
    if not game_over[0]:
        return

    import pygame
    font = pygame.font.Font(None, 72)
    text = "YOU WIN" if victory[0] else "GAME OVER"
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen = pygame.display.get_surface()
    screen.blit(text_surface, text_rect)

pn.on_update(control)
pn.on_update(move_invaders)
pn.on_update(check_collisions)
pn.on_update(check_player_hit)
pn.on_update(show_end_message)

game = pn.Game(WIDTH, HEIGHT)
game.start()
