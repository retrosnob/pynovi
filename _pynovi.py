import pygame
import math

pygame.init()
pygame.mixer.init()

# Internal data store
_entities = []
_entity_behaviors = []
_key_cooldowns = {}
_keys_pressed = set()
_keys_released = set()
_keys_held = {}  # Tracks when key was last physically pressed
_last_accepted_press_frame = {}  # Tracks when the key was last allowed through cooldown
_frame_count = 0
_sounds = {}
_game_over = False
_end_message = None  # <-- new
_mouse_position = (0, 0)
_mouse_buttons_down = set()
_mouse_buttons_released = set()

# Constants
KEY_MAP = {
    "up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT,
    "space": pygame.K_SPACE, "escape": pygame.K_ESCAPE, "w": pygame.K_w, "s": pygame.K_s
}

MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3

# Core API
class Entity:
    def __init__(self, x, y, width=50, height=50, color=(255, 0, 0), dx=0, dy=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.dx = dx
        self.dy = dy
        self.alive = True

    def update(self):
        self.x += self.dx
        self.y += self.dy

        # Automatically destroy entity if it moves outside screen bounds
        if self.y < -self.height or self.y > 600 or self.x < -self.width or self.x > 800:
            self.alive = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def is_touching(self, other_entity):
        return (
            self.x < other_entity.x + other_entity.width and
            self.x + self.width > other_entity.x and
            self.y < other_entity.y + other_entity.height and
            self.y + self.height > other_entity.y
        )

def create_entity(**kwargs):
    entity = Entity(**kwargs)
    _entities.append(entity)
    return entity

def on_update(update_function):
    _entity_behaviors.append(update_function)

def set_key_cooldown(key_name, frames):
    key = KEY_MAP.get(key_name)
    if key:
        _key_cooldowns[key] = frames

def is_key_pressed(key_name):
    key = KEY_MAP.get(key_name)
    if key is None:
        return False

    if key in _keys_held:
        cooldown = _key_cooldowns.get(key, 0)
        last_used = _last_accepted_press_frame.get(key, -9999)
        if _frame_count - last_used >= cooldown:
            _last_accepted_press_frame[key] = _frame_count
            return True
        return False

    return key in _keys_pressed

def get_mouse_position():
    return _mouse_position

def is_mouse_pressed(button=1):
    # Has the button been pressed this frame
    return button in _mouse_buttons_down

def is_mouse_released(button=1):
    return button in _mouse_buttons_released

def is_mouse_held(button=1):
    # Is the button down
    return pygame.mouse.get_pressed()[button - 1]  # button is 1 (left), 2 (middle), 3 (right)

def get_all():
    return [entity for entity in _entities if entity.alive]

def destroy(entity):
    entity.alive = False

def load_sound(name, path):
    _sounds[name] = pygame.mixer.Sound(path)

def play_sound(name):
    if name in _sounds:
        _sounds[name].play()

def end_game(message=None):
    global _game_over, _end_message
    _game_over = True
    _end_message = message

def draw_text(text, x, y, size=30, color=(255, 255, 255), center=False):
    font = pygame.font.Font(None, size)
    surface = pygame.display.get_surface()
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(text_surface, rect)

# Game loop
class Game:
    def __init__(self, width=800, height=600, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Entity Game")
        self.clock = pygame.time.Clock()
        self.running = False

    def start(self):
        global _frame_count
        self.running = True
        while self.running:
            _frame_count += 1
            _handle_events()
            self.screen.fill((0, 0, 0))

            if not _game_over:
                for update_function in _entity_behaviors:
                    update_function()

                global _entities
                _entities = [entity for entity in _entities if entity.alive]

                for entity in get_all():
                    entity.update()
                    entity.draw(self.screen)

            # Draw persistent end-of-game message if present
            if _game_over and _end_message:
                draw_text(_end_message, self.width // 2, self.height // 2, size=72, color=(255, 255, 255), center=True)

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()

def _handle_events():
    _keys_pressed.clear()
    _mouse_buttons_down.clear()
    _mouse_buttons_released.clear()

    global _mouse_position
    _mouse_position = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            _keys_pressed.add(event.key)
            _keys_held[event.key] = _frame_count
        elif event.type == pygame.KEYUP:
            _keys_pressed.discard(event.key)
            _keys_released.add(event.key)
            if event.key in _keys_held:
                del _keys_held[event.key]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            _mouse_buttons_down.add(event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            _mouse_buttons_released.add(event.button)

    _keys_released.clear()  # ✅ must remain at the end of the function

