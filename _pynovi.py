import pygame
import math

pygame.init()
pygame.mixer.init()

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------

KEY_MAP = {
    "up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT,
    "space": pygame.K_SPACE, "escape": pygame.K_ESCAPE, "w": pygame.K_w, "s": pygame.K_s
}

# -------------------------------------------------------------------
# Internal Input Manager (Not exposed to students)
# -------------------------------------------------------------------

class InputManager:
    def __init__(self):
        self.keys_pressed = set()
        self.keys_released = set()
        self.keys_held = {}
        self.last_accepted_press_frame = {}
        self.key_cooldowns = {}

        self.mouse_buttons_down = set()
        self.mouse_buttons_released = set()
        self.mouse_position = (0, 0)

    def update(self, frame_count):
        self.keys_pressed.clear()
        self.mouse_buttons_down.clear()
        self.mouse_buttons_released.clear()
        self.mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                self.keys_held[event.key] = frame_count
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
                self.keys_released.add(event.key)
                if event.key in self.keys_held:
                    del self.keys_held[event.key]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_buttons_down.add(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_buttons_released.add(event.button)

        self.keys_released.clear()

    def is_key_pressed(self, key_name, frame_count):
        key = KEY_MAP.get(key_name)
        if key is None:
            return False
        if key in self.keys_held:
            cooldown = self.key_cooldowns.get(key, 0)
            last_used = self.last_accepted_press_frame.get(key, -9999)
            if frame_count - last_used >= cooldown:
                self.last_accepted_press_frame[key] = frame_count
                return True
            return False
        return key in self.keys_pressed

    def is_key_held(self, key_name):
        key = KEY_MAP.get(key_name)
        return key in self.keys_held

    def set_key_cooldown(self, key_name, frames):
        key = KEY_MAP.get(key_name)
        if key:
            self.key_cooldowns[key] = frames

    def is_mouse_pressed(self, button):
        return button in self.mouse_buttons_down

    def is_mouse_released(self, button):
        return button in self.mouse_buttons_released

    def is_mouse_held(self, button):
        return pygame.mouse.get_pressed()[button - 1]

    def get_mouse_position(self):
        return self.mouse_position


_input = InputManager()

# -------------------------------------------------------------------
# Input functions exposed to students
# -------------------------------------------------------------------

def is_key_pressed(key_name):
    return _input.is_key_pressed(key_name, _frame_count)

def is_key_held(key_name):
    return _input.is_key_held(key_name)

def set_key_cooldown(key_name, frames):
    _input.set_key_cooldown(key_name, frames)

def is_mouse_pressed(button):
    return _input.is_mouse_pressed(button)

def is_mouse_held(button):
    return _input.is_mouse_held(button)

def is_mouse_released(button):
    return _input.is_mouse_released(button)

def get_mouse_position():
    return _input.get_mouse_position()

# -------------------------------------------------------------------
# Internal data store for entities and game state
# -------------------------------------------------------------------

_entities = []
_entity_behaviors = []
_frame_count = 0
_sounds = {}
_game_over = False
_end_message = None

# -------------------------------------------------------------------
# Entity system
# -------------------------------------------------------------------

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

# -------------------------------------------------------------------
# Entity API
# -------------------------------------------------------------------

def create_entity(**kwargs):
    entity = Entity(**kwargs)
    _entities.append(entity)
    return entity

def destroy(entity):
    entity.alive = False

def get_all():
    return [entity for entity in _entities if entity.alive]

def on_update(update_function):
    _entity_behaviors.append(update_function)

# -------------------------------------------------------------------
# Sound and text
# -------------------------------------------------------------------

def load_sound(name, path):
    _sounds[name] = pygame.mixer.Sound(path)

def play_sound(name):
    if name in _sounds:
        _sounds[name].play()

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

# -------------------------------------------------------------------
# Game control
# -------------------------------------------------------------------

def end_game(message=None):
    global _game_over, _end_message
    _game_over = True
    _end_message = message

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
        global _frame_count, _entities
        self.running = True
        while self.running:
            _frame_count += 1
            _input.update(_frame_count)
            self.screen.fill((0, 0, 0))

            if not _game_over:
                for update_function in _entity_behaviors:
                    update_function()

                _entities = [entity for entity in _entities if entity.alive]

                for entity in get_all():
                    entity.update()
                    entity.draw(self.screen)

            if _game_over and _end_message:
                draw_text(_end_message, self.width // 2, self.height // 2, size=72, color=(255, 255, 255), center=True)

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
