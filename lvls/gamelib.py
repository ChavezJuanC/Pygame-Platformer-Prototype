"""
This is the base module for the game. It creates all the main functions and
classes needed to create levels with just a few lines of code
"""

import pygame
from os import listdir
from os.path import isfile, join
import time

# Constants
PLAYER_VEL = 5
pygame.init()
pygame.mixer.init()

jump_sound = pygame.mixer.Sound(join("assets", "sounds", "jump.wav"))
hurt_sound = pygame.mixer.Sound(join("assets", "sounds", "hurt.wav"))
coin_collected = pygame.mixer.Sound(join("assets", "sounds", "coin.wav"))

score_font = pygame.font.SysFont("Bauhaus 93", 50)
# Screen dimensions
WIDTH, HEIGHT = 1920, 1080
window = pygame.display.set_mode((WIDTH, HEIGHT))

starting_lifes = 3

last_timmer = None


def draw_text(text, font, text_col):
    img = font.render(text, True, text_col)
    return img


def draw_life():
    img = pygame.image.load(join("assets", "Lifes", "life.png")).convert_alpha()
    return img


def flip(sprites):
    """
    Flip the sprites horizontally.
    """
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    """
    Load sprite sheets from a specified directory, splitting them into individual sprites.
    """
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []

        # Split the sprite sheet into individual sprites
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, depth=32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[f"{image.replace('.png', '')}_right"] = sprites
            all_sprites[f"{image.replace('.png', '')}_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size, sx, sy):
    """
    Retrieve and scale a block image from the terrain sprite sheet.
    """
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, depth=32)
    ##272, 64
    rect = pygame.Rect(sx, sy, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


def get_coin(size, sx, sy):
    path = join("assets", "Coins", "Normal", "goldcoin.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, depth=32)
    rect = pygame.Rect(sx, sy, size, size)
    surface.blit(image, (0, 0), rect)
    return surface


class Player(pygame.sprite.Sprite):
    SPRITES = load_sprite_sheets("MainCharacters", "VirtualGuy", 32, 32, True)
    COLOR = (0, 0, 200)
    GRAVITY = 1
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.animation_count = 0
        self.direction = "right"
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def jump(self):
        """
        Make the player jump by setting the vertical velocity.
        """
        jump_sound.play()
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1

        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        """
        Move the player by a specified amount.
        """
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        """
        Set the player to hit state.
        """
        self.hit = True
        hurt_sound.play()

    def move_left(self, vel):
        """
        Move the player to the left.
        """
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        """
        Move the player to the right.
        """
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        """
        Update the player's state each frame.
        """
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        """
        Reset the player's state when landing.
        """
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        """
        Reverse the player's vertical velocity when hitting head.
        """
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        """
        Update the player's sprite based on the current state.
        """
        sprite_sheet = "idle"

        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = f"{sprite_sheet}_{self.direction}"
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)

        self.sprite = sprites[sprite_index]
        self.animation_count += 1

        self.update()

    def update(self):
        """
        Update the player's rectangle and mask.
        """
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, window, offset):
        """
        Draw the player on the window.
        """
        window.blit(self.sprite, (self.rect.x - offset, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height

        self.name = name

    def draw(self, window, offset):
        """
        Draw the object on the window.
        """
        window.blit(self.image, (self.rect.x - offset, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size, sx, sy):
        super().__init__(x, y, size, size)
        block = get_block(size, sx, sy)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Coin(Object):
    def __init__(self, x, y, size, sx, sy, coin_id):
        super().__init__(x, y, size, size, name="coin")
        coin_block = get_coin(size, sx, sy)
        self.image.blit(coin_block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.coin_id = coin_id


class Trap(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, type):
        super().__init__(x, y, width, height, name="trap")
        self.trap = load_sprite_sheets("Traps", type, width, height)
        self.image = self.trap["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        """
        Turn the trap animation on.
        """
        self.animation_name = "on"

    def off(self):
        """
        Turn the trap animation off.
        """
        self.animation_name = "off"

    def loop(self):
        """
        Update the trap animation each frame.
        """
        sprites = self.trap[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)

        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


def handle_vertical_collision(player, objects, dy):
    """
    Handle vertical collisions for the player.
    """
    collided_objects = []

    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            if dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    """
    Check for collisions when moving horizontally.
    """
    player.move(dx, 0)
    player.update()
    collided_object = None

    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects, coin_list, window, background_img, offset):

    global player_score, starting_lifes, last_timmer

    """
    Handle player movement and collisions.
    """
    keys = pygame.key.get_pressed()
    player.x_vel = 0

    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)
    elif keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)
    elif keys[pygame.K_s]:
        player.x_vel = 0

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj:
            if obj.name == "trap":
                player.make_hit()
                if last_timmer == None:
                    starting_lifes -= 1
                    last_timmer = time.time()
                elif time.time() - last_timmer >= 2:
                    starting_lifes -= 1
                    last_timmer = time.time()
                    
            if len(coin_list) > 0 and obj.name == "coin":
                print("coin id" + str(obj.coin_id))
                coin_list_len = len(coin_list)
                index = next(
                    (
                        i
                        for i, object in enumerate(coin_list)
                        if object.coin_id == obj.coin_id
                    ),
                    None,
                )
                if index != None:
                    coin_list.pop(index)
                # add draw with req args# add window, bg and offset
                objects[-coin_list_len:] = coin_list
                coin_collected.play()
                draw(window, background_img, player, objects, offset, coin_list)


def get_background(name):
    """
    Load a background image.
    """
    image = pygame.image.load(join("assets", "Background", name))
    return image


def draw(window, background_img, player, objects, offset, coin_list):
    global life_x
    """
    Draw the game scene.
    """
    coin_coins = "COINS" if len(coin_list) != 1 else "COIN"
    score = draw_text(
        "{} - {}".format(len(coin_list), coin_coins), score_font, (225, 225, 225)
    )
    window.blit(background_img, (0, 0))

    for obj in objects:
        obj.draw(window, offset)

    window.blit(score, (WIDTH // 2, 30))

    ##game over??##
    if starting_lifes == 0:
        print("GAME OVER")
        pygame.quit()
        quit()
        
    lifes = [*[draw_life() for i in range(starting_lifes)]]

    life_x = 50

    for life in lifes:
        window.blit(life, (life_x, 50))
        life_x += 100
    player.draw(window, offset)
    pygame.display.update()


def build_wall(start_y, end_y, step, x_range, block_size, height, block_sx, block_sy):
    wall_list = []
    for i in range(start_y, end_y, step):
        for j in range(x_range):
            wall_list.append(
                Block(
                    block_size * i,
                    height - block_size * j,
                    block_size,
                    block_sx,
                    block_sy,
                )
            )
    return wall_list


def many_coins(
    start_x, end_x, start_id, height, block_size, coin_size, coin_sx, coin_sy
):
    coin_list = []
    for i in range(start_x, end_x):
        start_id = start_id
        new_coin = Coin(
            block_size * i + (coin_size // 2),
            height - block_size - coin_size,
            coin_size,
            coin_sx,
            coin_sy,
            coin_id=start_id,
        )
        coin_list.append(new_coin)
        start_id += 1

    return coin_list


def main():
    print("USE AS MODULE!")


if __name__ == "__main__":
    main()
