# -------------------------------------------------------------------
# Library Imports
# -------------------------------------------------------------------
import _pynovi as pn


# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
ASSETS_FOLDER = "" # A good idea is to give it the same name (minus .py) as your game file
WIDTH, HEIGHT = 800, 600

# Add any other constants here

# -------------------------------------------------------------------
# Global Variables
# -------------------------------------------------------------------



# -------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------



# -------------------------------------------------------------------
# Main Program
# -------------------------------------------------------------------

# In this section you will do things like:
#   Create entities
#   Load sounds
#   Register some or all of the functions with the API; it will call them, in order, every frame.


game = pn.Game(WIDTH, HEIGHT)
game.start()
