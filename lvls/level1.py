import pygame
from gamelib import (
    get_background,
    draw,
    build_wall,
    handle_move,
    many_coins,
    Block,
    Trap,
    Player,
)

LEVEL = 1
pygame.init()
pygame.display.set_caption("Platformer")
WIDTH, HEIGHT = 1920, 1080
FPS = 60
PLAYER_VEL = 5
window = pygame.display.set_mode((WIDTH, HEIGHT))


###spkies are 16 by 16
def main(window):
    """
    PLAYER AND FPS
    """
    clock = pygame.time.Clock()
    player = Player(50, 400, 32, 32)

    """
    Setting up the terrain specific for level
    """
    offset_x = 0
    scroll_area_width = 400
    background = get_background(name="city{}.png".format(LEVEL))
    block_size = 96

    ##floor
    block_sx, block_sy = 272, 64
    floor = [
        Block(i * block_size, HEIGHT - block_size, block_size, block_sx, block_sy)
        for i in range(-3, WIDTH * 5 // block_size)
    ]

    """
    TRAPS SECTION
    """
    fire_width = 16
    fire_height = 32
    fires = [
        ##x3
        *[
            Trap(
                block_size * 3 + i,
                HEIGHT - block_size - 64,
                fire_width,
                fire_height,
                "Fire",
            )
            for i in range(40, 160, 40)
        ],
        # x5
        *[
            Trap(
                block_size * 16 + i,
                HEIGHT - block_size * 3 - 64,
                fire_width,
                fire_height,
                "Fire",
            )
            for i in range(0, 200, 40)
        ],
        # x5
        *[
            Trap(
                block_size * 26 + i,
                HEIGHT - block_size - 64,
                fire_width,
                fire_height,
                "Fire",
            )
            for i in range(0, 200, 40)
        ],
        # x2
        Trap(
            block_size * 37 + 60,
            HEIGHT - block_size * 7 - 64,
            fire_width,
            fire_height,
            "Fire",
        ),
        Trap(block_size * 38, HEIGHT - block_size * 7 - 64, 16, 32, "Fire"),
        # x2 x2
        *[
            Trap(
                block_size * 52 + i,
                HEIGHT - block_size * 6 - 64,
                fire_width,
                fire_height,
                "Fire",
            )
            for i in range(0, 61, 60)
        ],
        *[
            Trap(
                block_size * 50 + i,
                HEIGHT - block_size * 6 - 64,
                fire_width,
                fire_height,
                "Fire",
            )
            for i in range(0, 61, 60)
        ],
        # x4
        *[
            Trap(
                block_size * 58 + i,
                HEIGHT - block_size - 64,
                fire_width,
                fire_height,
                "Fire",
            )
            for i in range(0, 161, 40)
        ],
        # x4
        *[
            Trap(
                block_size * 63 + i,
                HEIGHT - block_size - 64,
                fire_width,
                fire_height,
                "Fire",
            )
            for i in range(0, 161, 40)
        ],
        # x10
        *[
            Trap(
                block_size * 85 + i,
                HEIGHT - block_size * 3 - 64,
                fire_width,
                fire_height,
                "Fire",
            )
            for i in range(0, 160, 40)
        ],
        *[
            Trap(
                block_size * 89 + i,
                HEIGHT - block_size * 3 - 64,
                fire_width,
                fire_height,
                "Fire",
            )
            for i in range(40, 200, 40)
        ],
    ]

    for fire in fires:
        fire.on()

    """
    CREATING THE MAP
    """

    # containing walls
    starting_wall = build_wall(-4, -9, -1, 13, block_size, HEIGHT, block_sx, block_sy)
    end_wall = build_wall(100, 105, 1, 13, block_size, HEIGHT, block_sx, block_sy)

    ##terrain architechture blocks
    blocks = [
        ##start
        *starting_wall,
        Block(block_size * 2, HEIGHT - block_size * 2, block_size, block_sx, block_sy),
        # POI
        *[
            Block(
                block_size * i, HEIGHT - block_size * 3, block_size, block_sx, block_sy
            )
            for i in range(5, 10)
        ],
        # POI
        *[
            Block(
                block_size * 11, HEIGHT - block_size * i, block_size, block_sx, block_sy
            )
            for i in range(2, 6)
        ],
        *[
            Block(
                block_size * i, HEIGHT - block_size * 5, block_size, block_sx, block_sy
            )
            for i in range(12, 23)
        ],
        Block(block_size * 22, HEIGHT - block_size * 4, block_size, block_sx, block_sy),
        Block(block_size * 22, HEIGHT - block_size * 3, block_size, block_sx, block_sy),
        Block(block_size * 23, HEIGHT - block_size * 3, block_size, block_sx, block_sy),
        Block(block_size * 24, HEIGHT - block_size * 3, block_size, block_sx, block_sy),
        # POI
        *[
            Block(
                block_size * i, HEIGHT - block_size * 3, block_size, block_sx, block_sy
            )
            for i in range(13, 21)
        ],
        # POI
        Block(block_size * 29, HEIGHT - block_size * 4, block_size, block_sx, block_sy),
        Block(block_size * 29, HEIGHT - block_size * 3, block_size, block_sx, block_sy),
        Block(block_size * 30, HEIGHT - block_size * 2, block_size, block_sx, block_sy),
        Block(block_size * 30, HEIGHT - block_size * 3, block_size, block_sx, block_sy),
        # lader
        Block(block_size * 33, HEIGHT - block_size * 3, block_size, block_sx, block_sy),
        Block(block_size * 35, HEIGHT - block_size * 5, block_size, block_sx, block_sy),
        Block(block_size * 37, HEIGHT - block_size * 7, block_size, block_sx, block_sy),
        Block(block_size * 38, HEIGHT - block_size * 7, block_size, block_sx, block_sy),
        # bridge
        *[
            Block(
                block_size * i, HEIGHT - block_size * 8, block_size, block_sx, block_sy
            )
            for i in range(42, 46)
        ],
        # tunnel-left----pick up here----
        Block(block_size * 50, HEIGHT - block_size * 2, block_size, block_sx, block_sy),
        Block(block_size * 50, HEIGHT - block_size * 3, block_size, block_sx, block_sy),
        Block(block_size * 50, HEIGHT - block_size * 4, block_size, block_sx, block_sy),
        Block(block_size * 50, HEIGHT - block_size * 5, block_size, block_sx, block_sy),
        Block(block_size * 50, HEIGHT - block_size * 5, block_size, block_sx, block_sy),
        Block(block_size * 50, HEIGHT - block_size * 6, block_size, block_sx, block_sy),
        # tunnel-right
        *[
            Block(
                block_size * 52, HEIGHT - block_size * i, block_size, block_sx, block_sy
            )
            for i in range(3, 7)
        ],
        # tunnel-exit
        *[
            Block(
                block_size * i, HEIGHT - block_size * 3, block_size, block_sx, block_sy
            )
            for i in range(53, 57)
        ],
        # section
        *[
            Block(
                block_size * i, HEIGHT - block_size * 3, block_size, block_sx, block_sy
            )
            for i in range(67, 71)
        ],
        # climb-left
        *[
            Block(
                block_size * 73, HEIGHT - block_size * i, block_size, block_sx, block_sy
            )
            for i in range(3, 10)
        ],
        # cimb-right
        *[
            Block(
                block_size * 76, HEIGHT - block_size * i, block_size, block_sx, block_sy
            )
            for i in range(2, 10)
        ],
        # steps
        Block(block_size * 74, HEIGHT - block_size * 3, block_size, block_sx, block_sy),
        Block(block_size * 75, HEIGHT - block_size * 5, block_size, block_sx, block_sy),
        Block(block_size * 74, HEIGHT - block_size * 7, block_size, block_sx, block_sy),
        Block(block_size * 75, HEIGHT - block_size * 9, block_size, block_sx, block_sy),
        # large jump - left
        *[
            Block(
                block_size * i, HEIGHT - block_size * 6, block_size, block_sx, block_sy
            )
            for i in range(81, 86)
        ],
        ###
        # large jump - right
        *[
            Block(
                block_size * i, HEIGHT - block_size * 6, block_size, block_sx, block_sy
            )
            for i in range(90, 95)
        ],
        Block(block_size * 90, HEIGHT - block_size * 6, block_size, block_sx, block_sy),
        Block(block_size * 91, HEIGHT - block_size * 6, block_size, block_sx, block_sy),
        Block(block_size * 92, HEIGHT - block_size * 6, block_size, block_sx, block_sy),
        Block(block_size * 93, HEIGHT - block_size * 6, block_size, block_sx, block_sy),
        Block(block_size * 94, HEIGHT - block_size * 6, block_size, block_sx, block_sy),
        # ending
        *end_wall,
    ]
    """
    Coins
    """
    coin_size = 64
    coin_sx, coin_sy = 0, 0

    coins = [
        *many_coins(5, 10, 0, HEIGHT, block_size, coin_size, coin_sx, coin_sy),
        *many_coins(
            13, 16, 5, HEIGHT - block_size * 2, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            18, 21, 8, HEIGHT - block_size * 2, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(28, 30, 11, HEIGHT, block_size, coin_size, coin_sx, coin_sy),
        *many_coins(
            33, 34, 13, HEIGHT - block_size * 2, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            35, 36, 14, HEIGHT - block_size * 4, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            42, 46, 15, HEIGHT - block_size * 7, block_size, coin_size, coin_sx, coin_sy
        ),
        ##drop
        *many_coins(
            51, 52, 19, HEIGHT - block_size * 5, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            51, 52, 20, HEIGHT - block_size * 4, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            51, 52, 21, HEIGHT - block_size * 3, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            51, 52, 22, HEIGHT - block_size * 2, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            51, 52, 23, HEIGHT - block_size, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(51, 52, 24, HEIGHT, block_size, coin_size, coin_sx, coin_sy),
        *many_coins(
            53, 57, 25, HEIGHT - block_size * 2, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(60, 63, 29, HEIGHT, block_size, coin_size, coin_sx, coin_sy),
        *many_coins(
            67, 71, 32, HEIGHT - block_size * 2, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            81, 86, 36, HEIGHT - block_size * 5, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            90, 95, 41, HEIGHT - block_size * 5, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            87, 89, 46, HEIGHT - block_size * 3, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            87, 89, 48, HEIGHT - block_size * 2, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            87, 89, 50, HEIGHT - block_size, block_size, coin_size, coin_sx, coin_sy
        ),  # nextavial 52
    ]

    ##creating objects list
    objects = [*floor, *blocks, *fires, *coins]

    """
    MAIN LOOP
    """
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        ##loops
        player.loop(FPS)
        for fire in fires:
            fire.loop()

        ##movement
        handle_move(
            player=player,
            objects=objects,
            coin_list=coins,
            window=window,
            offset=offset_x,
            background_img=background,
        )

        ##draw to window
        draw(
            window=window,
            background_img=background,
            player=player,
            objects=objects,
            offset=offset_x,
            coin_list=coins,
        )
        ##scrolling bg
        if (
            (player.rect.right - offset_x >= WIDTH - scroll_area_width)
            and player.x_vel > 0
        ) or ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)

    """
    remove coin by setting a coin id and than removing by id from list
    than update screen to redraw updated list
    """
