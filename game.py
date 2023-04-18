import arcade
import level

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Подземелье"

CHARACTER_SCALING = 0.6

PLAYER_MOVEMENT_SPEED = 4
PLAYER_JUMP_SPEED = 17


class PlatformerGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.scene = None

        self.player_sprite = None

        self.physics_engine = None
        self.gui_camera = None

        self.idle_sprites = arcade.load_spritesheet('resources/player_idle.png', 84, 97, 3, 3)
        self.walk_sprites = arcade.load_spritesheet('resources/player_walk.png', 83, 95, 6, 6)

        self.idle_sprite_index = 0

        # Звуки (встроенные)
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin2.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump2.wav")
        self.death_sound = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.win_sound = arcade.load_sound(":resources:sounds/upgrade1.wav")

        # Загружаем фон
        self.background = arcade.load_texture("resources/background.png")

    def setup(self):
        self.gui_camera = arcade.camera.Camera(viewport_width=self.width, viewport_height=self.height)

        self.scene = arcade.Scene()

        # Анимация персонажа
        self.player_sprite = arcade.AnimatedWalkingSprite()
        self.player_sprite.walk_right_textures = self.walk_sprites
        self.player_sprite.walk_left_textures = self.walk_sprites
        self.player_sprite.scale = CHARACTER_SCALING

        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 96
        self.scene.add_sprite("Player", self.player_sprite)

        self.physics_engine = level.populate(self)

    def on_draw(self):
        arcade.start_render()

        # Рисуем фон на весь экран
        arcade.set_background_color(arcade.csscolor.WHITE)
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Рисуем все спрайты
        self.scene.draw()

        self.gui_camera.use()

        # Рисуем сколько монет осталось собрать
        arcade.draw_text(
            f"Осталось монет: {len(self.scene['Coins'])}",
            10,
            10,
            arcade.csscolor.BLACK,
            18,
        )

    def on_key_press(self, key, modifiers):
        # Механика прыжка и движения

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        # Механика прыжка и движения
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        # Не даем персонажу выйти за границы экрана
        if self.player_sprite.center_x < 0:
            self.player_sprite.center_x = 0
        if self.player_sprite.center_x > SCREEN_WIDTH:
            self.player_sprite.center_x = SCREEN_WIDTH

        if self.player_sprite.change_x == 0 and self.player_sprite.change_y == 0:

            self.idle_sprite_index += 0.05

            if self.idle_sprite_index >= len(self.idle_sprites):
                self.idle_sprite_index = 0

            self.player_sprite.texture = self.idle_sprites[int(self.idle_sprite_index)]
        else:
            self.player_sprite.update_animation(delta_time)

        # Обновляем физику
        self.physics_engine.update()

        # Проверяем столкновения
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        bomb_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Bombs"])

        if len(bomb_hit_list) > 0:
            # Мы попали в бомбу, поэтому убиваем игрока
            self.player_sprite.center_x = 64
            self.player_sprite.center_y = 96

            arcade.play_sound(self.death_sound)

            # Clear coins
            self.scene["Coins"].clear()
            level.add_coins(self)

        # Проверяем, собрали ли мы все монеты
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)

        if len(self.scene["Coins"]) == 0:
            # Мы собрали все монеты, поэтому перезапускаем уровень
            self.player_sprite.center_x = 64
            self.player_sprite.center_y = 96

            arcade.play_sound(self.win_sound)
            level.add_coins(self)


def main():
    window = PlatformerGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
