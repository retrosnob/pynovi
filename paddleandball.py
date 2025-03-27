# -------------------------------------------------------------------
# Library Imports
# -------------------------------------------------------------------
import _pynovi as pn

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
WIDTH, HEIGHT = 600, 400
BALL_SIZE = 20
BALL_COLOR = (255, 255, 0)
BALL_SPEED_X = 3
BALL_SPEED_Y = -4

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_COLOR = (0, 255, 0)
PADDLE_SPEED = 6

# -------------------------------------------------------------------
# Global Variables
# -------------------------------------------------------------------
ball = None
paddle = None
game_running = True

# -------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------
def control():
    """Move the paddle left and right."""
    if not game_running:
        return
    if pn.is_key_held("left") and paddle.x > 0:
        paddle.x -= PADDLE_SPEED
    if pn.is_key_held("right") and paddle.x + paddle.width < WIDTH:
        paddle.x += PADDLE_SPEED

def bounce_ball():
    """Bounce the ball off walls and paddle. End game if missed."""
    global game_running
    if not game_running:
        return

    # Bounce off side walls
    if ball.x <= 0 or ball.x + ball.width >= WIDTH:
        ball.dx *= -1

    # Bounce off top wall
    if ball.y <= 0:
        ball.dy *= -1

    # Bounce off paddle
    if ball.dy > 0 and ball.is_touching(paddle):
        ball.dy *= -1

    # Game over if ball falls below screen
    if ball.y > HEIGHT:
        game_running = False
        pn.end_game("GAME OVER")

# -------------------------------------------------------------------
# Main Program
# -------------------------------------------------------------------
paddle = pn.create_entity(
    x=WIDTH // 2 - PADDLE_WIDTH // 2,
    y=HEIGHT - PADDLE_HEIGHT - 10,
    width=PADDLE_WIDTH,
    height=PADDLE_HEIGHT,
    color=PADDLE_COLOR
)

ball = pn.create_entity(
    x=WIDTH // 2,
    y=HEIGHT // 2,
    width=BALL_SIZE,
    height=BALL_SIZE,
    color=BALL_COLOR,
    dx=BALL_SPEED_X,
    dy=BALL_SPEED_Y
)

pn.on_update(control)
pn.on_update(bounce_ball)

game = pn.Game(WIDTH, HEIGHT)
game.start()
