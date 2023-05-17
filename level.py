from arcade import PhysicsEnginePlatformer, SpriteList

import random
import arcade

TILE_SCALING = 0.4
COIN_SCALING = 0.2
BOMB_SCALING = 0.2
PLATFORM_SCALING = 0.3

GRAVITY = 1


class MoveDirection:
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


def populate(game) -> PhysicsEnginePlatformer:
    add_platform(game, ":resources:images/tiles/dirt.png", 0, 32, 3000)

    # Платформы сверху
    add_platform(game, ":resources:images/tiles/boxCrate_double.png", 90, 180, 300 - 90)
    add_platform(game, ":resources:images/tiles/boxCrate_double.png", 350, 250, 400 - 350,
                 move_direction=MoveDirection.UP)

    add_platform(game, ":resources:images/tiles/boxCrate_double.png", 500, 350, 800 - 500,
                 move_direction=MoveDirection.LEFT)

    add_platform(game, ":resources:images/tiles/boxCrate_double.png", 900, 450, 1000 - 900,
                 move_direction=MoveDirection.DOWN)

    add_platform(game, ":resources:images/tiles/boxCrate_double.png", 1100, 350, 1300 - 1100,
                 move_direction=MoveDirection.RIGHT)

    add_platform(game, ":resources:images/tiles/boxCrate_double.png", 1550, 350, 1800 - 1550,
                 move_direction=MoveDirection.LEFT)

    game.scene.add_sprite("Bombs", arcade.Sprite("resources/bomb.png", BOMB_SCALING, center_x=130, center_y=220))
    game.scene.add_sprite("Bombs", arcade.Sprite("resources/bomb.png", BOMB_SCALING, center_x=520, center_y=390))
    game.scene.add_sprite("Bombs", arcade.Sprite("resources/bomb.png", BOMB_SCALING, center_x=1200, center_y=400))

    repopulate_tiles(game)

    return arcade.PhysicsEnginePlatformer(
        game.player_sprite, gravity_constant=GRAVITY, walls=game.scene["Walls"], platforms=game.scene["Platforms"]
    )


def repopulate_tiles(game):
    fill_with_tiles(game, ":resources:images/items/coinGold.png", 90, 300 - 90, 180, "Coins", 5, COIN_SCALING)
    fill_with_tiles(game, ":resources:images/items/coinGold.png", 350, 400 - 350, 250, "Coins", 4, COIN_SCALING)
    fill_with_tiles(game, ":resources:images/items/coinGold.png", 500, 800 - 500, 350, "Coins", 4, COIN_SCALING)
    fill_with_tiles(game, ":resources:images/items/coinGold.png", 900, 1000 - 900, 450, "Coins", 4, COIN_SCALING)
    fill_with_tiles(game, ":resources:images/items/coinGold.png", 1100, 1200 - 1100, 350, "Coins", 4, COIN_SCALING)
    fill_with_tiles(game, ":resources:images/items/coinGold.png", 1400, 1500 - 1400, 350, "Coins", 4, COIN_SCALING)


def fill_with_tiles(game, filename, from_x, length, y, sprite_list_name, count=10, scale=TILE_SCALING):
    for _ in range(count):
        x = random.randrange(from_x, from_x + length, 32)

        # check collision with bombs
        if arcade.check_for_collision_with_list(
                arcade.Sprite(filename, scale, center_x=x, center_y=y + 40),
                game.scene["Bombs"]
        ):
            continue

        tile = arcade.Sprite(filename, scale)
        tile.center_x = x
        tile.center_y = y + 40

        game.scene.add_sprite(sprite_list_name, tile)


def add_platform(game,
                 filename, x, y,
                 length=100,
                 move_direction=None):
    for x in range(x, x + length, 32):
        wall = arcade.Sprite(filename, PLATFORM_SCALING)
        wall.center_x = x
        wall.center_y = y

        if move_direction is not None:
            wall.change_x = move_direction[0]
            wall.change_y = move_direction[1]

            wall.boundary_left = x - 100
            wall.boundary_right = x + 100
            wall.boundary_top = y + 100
            wall.boundary_bottom = y - 100
            game.scene.add_sprite("Platforms", wall)
        else:
            game.scene.add_sprite("Walls", wall)
