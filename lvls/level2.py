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

LEVEL = 2
pygame.init()
pygame.display.set_caption("Platformer")
WIDTH, HEIGHT = 1920, 1080
FPS = 60
PLAYER_VEL = 5
window = pygame.display.set_mode((WIDTH, HEIGHT))


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
    block_sx, block_sy = 0, 64

    floor = [
        Block(i * block_size, HEIGHT - block_size, block_size, block_sx, block_sy)
        for i in range(-3, WIDTH * 5 // block_size)
    ]

    """
    TRAPS SECTION
    """
    saw_width = 38
    saw_height = 38

    saw_traps = [
        # x3
        *[
            Trap(block_size * i, HEIGHT - block_size * 2, saw_width, saw_height, "Saw")
            for i in range(2, 8, 2)
        ],
        # x4
        *[
            Trap(block_size * i, HEIGHT - block_size * 2, saw_width, saw_height, "Saw")
            for i in range(32, 36)
        ],
        # x4
        *[
            Trap(block_size * i, HEIGHT - block_size * 4, saw_width, saw_height, "Saw")
            for i in range(44, 47)
        ],
        *[
            Trap(block_size * i, HEIGHT - block_size * 4, saw_width, saw_height, "Saw")
            for i in range(49, 52)
        ],
        *[
            Trap(block_size * i, HEIGHT - block_size * 2, saw_width, saw_height, "Saw")
            for i in range(66, 68)
        ],
        *[
            Trap(block_size * i, HEIGHT - block_size * 2, saw_width, saw_height, "Saw")
            for i in range(70, 72)
        ],
        *[
            Trap(block_size * i, HEIGHT - block_size * 2, saw_width, saw_height, "Saw")
            for i in range(74, 76)
        ],
        Trap(block_size * 81, HEIGHT - block_size * 4, saw_width, saw_height, "Saw"),
        Trap(block_size * 85, HEIGHT - block_size * 6, saw_width, saw_height, "Saw"),
        Trap(block_size * 93, HEIGHT - block_size * 6, saw_width, saw_height, "Saw"),
        Trap(block_size * 97, HEIGHT - block_size * 4, saw_width, saw_height, "Saw"),
    ]

    for saw in saw_traps:
        saw.on()

    """
    CREATING THE MAP
    """

    ending_wall = build_wall(100, 105, 1, 13, block_size, HEIGHT, block_sx, block_sy)

    start_wall = build_wall(-4, -9, -1, 13, block_size, HEIGHT, block_sx, block_sy)

    blocks = [
        ##start
        *start_wall,
        # POI
        *[
            Block(
                block_size * i, HEIGHT - block_size * 2, block_size, block_sx, block_sy
            )
            for i in range(9, 13)
        ],
        # steps
        Block(block_size * 17, HEIGHT - block_size * 3, block_size, block_sx, block_sy),
        Block(block_size * 20, HEIGHT - block_size * 5, block_size, block_sx, block_sy),
        Block(block_size * 23, HEIGHT - block_size * 7, block_size, block_sx, block_sy),
        # entrance1
        *[
            Block(
                block_size * i, HEIGHT - block_size * 11, block_size, block_sx, block_sy
            )
            for i in range(27, 35)
        ],
        *[
            Block(
                block_size * i, HEIGHT - block_size * 9, block_size, block_sx, block_sy
            )
            for i in range(27, 33)
        ],
        ##exit1
        *[
            Block(
                block_size * 32, HEIGHT - block_size * i, block_size, block_sx, block_sy
            )
            for i in range(6, 9)
        ],
        *[
            Block(
                block_size * 34, HEIGHT - block_size * i, block_size, block_sx, block_sy
            )
            for i in range(6, 11)
        ],
        # bridge
        Block(block_size * 39, HEIGHT - block_size * 2, block_size, block_sx, block_sy),
        Block(block_size * 40, HEIGHT - block_size * 3, block_size, block_sx, block_sy),
        Block(block_size * 41, HEIGHT - block_size * 4, block_size, block_sx, block_sy),
        Block(block_size * 42, HEIGHT - block_size * 4, block_size, block_sx, block_sy),
        Block(block_size * 43, HEIGHT - block_size * 4, block_size, block_sx, block_sy),
        *[
            Block(
                block_size * i, HEIGHT - block_size * 4, block_size, block_sx, block_sy
            )
            for i in range(47, 49)
        ],
        *[
            Block(
                block_size * i, HEIGHT - block_size * 4, block_size, block_sx, block_sy
            )
            for i in range(52, 54)
        ],
        Block(block_size * 54, HEIGHT - block_size * 4, block_size, block_sx, block_sy),
        Block(block_size * 55, HEIGHT - block_size * 3, block_size, block_sx, block_sy),
        Block(block_size * 56, HEIGHT - block_size * 2, block_size, block_sx, block_sy),
        # climb-left
        *[
            Block(
                block_size * 60, HEIGHT - block_size * i, block_size, block_sx, block_sy
            )
            for i in range(3, 10)
        ],
        # climb-right
        *[
            Block(
                block_size * 63, HEIGHT - block_size * i, block_size, block_sx, block_sy
            )
            for i in range(2, 10)
        ],
        # steps
        Block(block_size * 61, HEIGHT - block_size * 3, block_size, block_sx, block_sy),
        Block(block_size * 62, HEIGHT - block_size * 5, block_size, block_sx, block_sy),
        Block(block_size * 61, HEIGHT - block_size * 7, block_size, block_sx, block_sy),
        Block(block_size * 62, HEIGHT - block_size * 9, block_size, block_sx, block_sy),
        # last pyramid
        *[
            Block(
                block_size * i, HEIGHT - block_size * 2, block_size, block_sx, block_sy
            )
            for i in range(80, 83)
        ],
        *[
            Block(
                block_size * i, HEIGHT - block_size * 3, block_size, block_sx, block_sy
            )
            for i in range(80, 83)
        ],
        *[
            Block(
                block_size * i, HEIGHT - block_size * 5, block_size, block_sx, block_sy
            )
            for i in range(84, 87)
        ],
        *[
            Block(
                block_size * i, HEIGHT - block_size * 7, block_size, block_sx, block_sy
            )
            for i in range(88, 91)
        ],
        Block(block_size * 89, HEIGHT - block_size * 9, block_size, block_sx, block_sy),
        *[
            Block(
                block_size * i, HEIGHT - block_size * 5, block_size, block_sx, block_sy
            )
            for i in range(92, 95)
        ],
        *[
            Block(
                block_size * i, HEIGHT - block_size * 3, block_size, block_sx, block_sy
            )
            for i in range(96, 99)
        ],
        *[
            Block(
                block_size * i, HEIGHT - block_size * 2, block_size, block_sx, block_sy
            )
            for i in range(96, 99)
        ],
        *ending_wall,
    ]
    coin_size = 64
    coin_sx, coin_sy = 0, 0

    coins = [
        *many_coins(
            9, 13, 0, HEIGHT - block_size, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            17, 18, 4, HEIGHT - block_size * 2, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            20, 21, 5, HEIGHT - block_size * 4, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            23, 24, 6, HEIGHT - block_size * 6, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            27, 33, 7, HEIGHT - block_size * 8, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            33, 34, 13, HEIGHT - block_size * 8, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            33, 34, 14, HEIGHT - block_size * 7, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            33, 34, 15, HEIGHT - block_size * 6, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            33, 34, 16, HEIGHT - block_size * 5, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            33, 34, 17, HEIGHT - block_size * 4, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            33, 34, 18, HEIGHT - block_size * 3, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            33, 34, 19, HEIGHT - block_size * 2, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            41, 44, 20, HEIGHT - block_size * 3, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            47, 49, 23, HEIGHT - block_size * 3, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            52, 55, 25, HEIGHT - block_size * 3, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            62, 64, 28, HEIGHT - block_size * 8, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(64, 66, 30, HEIGHT, block_size, coin_size, coin_sx, coin_sy),
        *many_coins(68, 70, 32, HEIGHT, block_size, coin_size, coin_sx, coin_sy),
        *many_coins(72, 74, 34, HEIGHT, block_size, coin_size, coin_sx, coin_sy),
        *many_coins(76, 80, 36, HEIGHT, block_size, coin_size, coin_sx, coin_sy),
        *many_coins(
            88, 91, 40, HEIGHT - block_size * 6, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            89, 90, 43, HEIGHT - block_size * 8, block_size, coin_size, coin_sx, coin_sy
        ),
        *many_coins(
            99,
            100,
            44,
            HEIGHT - block_size * 5,
            block_size,
            coin_size,
            coin_sx,
            coin_sy,
        ),
        *many_coins(
            99,
            100,
            45,
            HEIGHT - block_size * 4,
            block_size,
            coin_size,
            coin_sx,
            coin_sy,
        ),
        *many_coins(
            99,
            100,
            46,
            HEIGHT - block_size * 3,
            block_size,
            coin_size,
            coin_sx,
            coin_sy,
        ),
        *many_coins(
            99,
            100,
            47,
            HEIGHT - block_size * 2,
            block_size,
            coin_size,
            coin_sx,
            coin_sy,
        ),
        *many_coins(
            99, 100, 48, HEIGHT - block_size, block_size, coin_size, coin_sx, coin_sy
        ),
    ]  # 44

    ##creating objects list
    objects = [*floor, *blocks, *saw_traps, *coins]

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

        for saw in saw_traps:
            saw.loop()

        ##movement
        handle_move(
            player=player,
            objects=objects,
            coin_list=coins,
            window=window,
            background_img=background,
            offset=offset_x,
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
