import pygame
from gamelib import get_background, draw

LEVEL = 3
pygame.init()
pygame.display.set_caption("Platformer")
WIDTH, HEIGHT = 1920, 1080
FPS = 60
PLAYER_VEL = 5
window = pygame.display.set_mode((WIDTH, HEIGHT))


def main(window):
    clock = pygame.time.Clock()
    run = True

    background = get_background(name="city{}.png".format(LEVEL))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window=window, background_img=background)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
