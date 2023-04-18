from arcade import PhysicsEnginePlatformer
from game import PlatformerGame

import arcade

TILE_SCALING = 0.4
COIN_SCALING = 0.2
BOMB_SCALING = 0.2
PLATFORM_SCALING = 0.3

GRAVITY = 1


def populate(game: PlatformerGame) -> PhysicsEnginePlatformer:
    for x in range(0, 1250, 32):
        wall = arcade.Sprite(":resources:images/tiles/dirt.png", TILE_SCALING)
        wall.center_x = x
        wall.center_y = 32

        game.scene.add_sprite("Walls", wall)

    for x in range(90, 300, 32):
        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", PLATFORM_SCALING)
        wall.center_x = x
        wall.center_y = 180

        game.scene.add_sprite("Walls", wall)

    for x in range(350, 400, 32):
        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", PLATFORM_SCALING)
        wall.center_x = x
        wall.center_y = 250

        wall.change_y = 1
        wall.boundary_top = 300
        wall.boundary_bottom = 200

        game.scene.add_sprite("Platforms", wall)

    for x in range(500, 700, 32):
        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", PLATFORM_SCALING)
        wall.center_x = x
        wall.center_y = 350

        wall.change_x = 1
        wall.boundary_left = 400
        wall.boundary_right = 800

        game.scene.add_sprite("Platforms", wall)

    for x in range(900, 1000, 32):
        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", PLATFORM_SCALING)
        wall.center_x = x
        wall.center_y = 450

        game.scene.add_sprite("Walls", wall)

    add_bombs(game)
    add_coins(game)

    return arcade.PhysicsEnginePlatformer(
        game.player_sprite, gravity_constant=GRAVITY, walls=game.scene["Walls"], platforms=game.scene["Platforms"]
    )


def add_coins(game: PlatformerGame):
    for x in range(90, 300, 190):
        coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
        coin.center_x = x
        coin.center_y = 220

        game.scene.add_sprite("Coins", coin)

    for x in range(350, 400, 30):
        coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
        coin.center_x = x
        coin.center_y = 280

        game.scene.add_sprite("Coins", coin)

    for x in range(700, 800, 50):
        coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
        coin.center_x = x
        coin.center_y = 390

        game.scene.add_sprite("Coins", coin)

    for x in range(400, 600, 100):
        coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
        coin.center_x = x
        coin.center_y = 390

        game.scene.add_sprite("Coins", coin)

    for x in range(900, 1000, 50):
        coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
        coin.center_x = x
        coin.center_y = 490

        game.scene.add_sprite("Coins", coin)


def add_bombs(game: PlatformerGame):
    game.scene.add_sprite("Bombs", arcade.Sprite("resources/bomb.png", BOMB_SCALING, center_x=170, center_y=220))
    game.scene.add_sprite("Bombs", arcade.Sprite("resources/bomb.png", BOMB_SCALING, center_x=600, center_y=400))
