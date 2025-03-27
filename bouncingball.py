# -------------------------------------------------------------------
# Library Imports
# -------------------------------------------------------------------
import _pynovi as pn

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
WIDTH, HEIGHT = 600, 400
BALL_SIZE = 30
BALL_COLOR = (255, 255, 0)
BALL_SPEED_X = 4
BALL_SPEED_Y = 3

# -------------------------------------------------------------------
# Global Variables
# -------------------------------------------------------------------
ball = None

# -------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------
def bounce_ball():
    """Update the ball's direction if it hits the screen edges."""
    if ball.x <= 0 or ball.x + ball.width >= WIDTH:
        ball.dx *= -1
    if ball.y <= 0 or ball.y + ball.height >= HEIGHT:
        ball.dy *= -1

# -------------------------------------------------------------------
# Main Program
# -------------------------------------------------------------------
ball = pn.create_entity(
    x=WIDTH // 2,
    y=HEIGHT // 2,
    width=BALL_SIZE,
    height=BALL_SIZE,
    color=BALL_COLOR,
    dx=BALL_SPEED_X,
    dy=BALL_SPEED_Y
)

pn.on_update(bounce_ball)

game = pn.Game(WIDTH, HEIGHT)
game.start()
