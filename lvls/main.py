"""
This is the main game GUI, MENU and Level Select and Start
"""

import level1, level2, pygame

LEVEL = 1
pygame.init()
pygame.display.set_caption("Platformer")
WIDTH, HEIGHT = 1920, 1080
FPS = 60
PLAYER_VEL = 5
window = pygame.display.set_mode((WIDTH, HEIGHT))

selection = input("Please select a level 1-2:")
if selection == str(1):
    level1.main(window)
elif selection == str(2):
    level2.main(window)
else:
    print("Invalid Choice")



    """
    create main loop that displays levels as buttons, on click start corresponding loop 
    and on game over come back to this loop. (import it on lvl ??? idk)
    """