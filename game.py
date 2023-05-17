import arcade
import level
import scores

from util.animation import SpriteAnimation

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

        self.scores = []
        self.last_score = None
        self.best_score = None

        self.player_sprite = None

        self.physics_engine = None
        self.gui_camera = None
        self.camera = None
        self.health = 20
        self.score = 0
        self.paused = True

        # Создаем кнопку старта
        self.start_button = arcade.Sprite("resources/start_button.png")
        self.start_button.scale = 0.5
        self.start_button.center_x = SCREEN_WIDTH // 2
        self.start_button.center_y = SCREEN_HEIGHT // 2 + 50

        self.current_player_animation = None

        self.idle_sprites = arcade.load_spritesheet('resources/player_idle.png', 84, 97, 3, 3)
        self.walk_sprites = arcade.load_spritesheet('resources/player_walk.png', 83, 95, 6, 6)
        self.death_sprites = arcade.load_spritesheet('resources/player_death.png', 94, 75, 4, 4)

        # Звуки (встроенные)
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin2.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump2.wav")
        self.death_sound = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.win_sound = arcade.load_sound(":resources:sounds/upgrade1.wav")
        self.hurt_sound = arcade.load_sound(":resources:sounds/hurt1.wav")

        # Загружаем фон
        self.background = arcade.load_texture("resources/background.png")

    def setup(self):
        self.gui_camera = arcade.camera.Camera(viewport_width=self.width, viewport_height=self.height)

        self.scene = arcade.Scene()
        self.camera = arcade.camera.Camera(viewport_width=self.width, viewport_height=self.height)

        # Анимация персонажа
        self.player_sprite = arcade.Sprite(scale=CHARACTER_SCALING)

        self.switch_animation(self.idle_sprites, 0.2)

        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 96

        self.scores = scores.get_scores()
        self.last_score = 0
        self.best_score = 0

        self.scene.add_sprite("Player", self.player_sprite)

        self.physics_engine = level.populate(self)

    def switch_animation(self, frames, delay=0.1, loop=True):
        if self.current_player_animation is not None and self.current_player_animation.textures == frames:
            return

        self.current_player_animation = SpriteAnimation(self.player_sprite, frames, delay, loop)

    def on_draw(self):
        arcade.start_render()

        # Рисуем фон на весь экран
        arcade.set_background_color(arcade.csscolor.WHITE)
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        self.camera.use()

        # Рисуем все спрайты
        self.scene.draw()

        self.gui_camera.use()

        if self.paused:
            # Рисуем кнопку старта
            self.start_button.draw()

            # Создаем надписи с очками
            arcade.draw_text(
                f"Последний счет: {self.last_score}",
                font_size=20,
                start_x=SCREEN_WIDTH // 2,
                start_y=SCREEN_HEIGHT // 2 - 170,
                anchor_x="center",
            )
            arcade.draw_text(
                f"Лучший счет: {self.best_score}",
                font_size=20,
                start_x=SCREEN_WIDTH // 2,
                start_y=SCREEN_HEIGHT // 2 - 200,
                anchor_x="center",
            )
            return

        # Рисуем сколько монет осталось собрать
        arcade.draw_text(
            f"Нужно собрать: {len(self.scene['Coins'])}",
            10,
            SCREEN_HEIGHT - 80,
            arcade.csscolor.WHITE,
            18,
        )
        # Рисуем монетку возле текста
        arcade.draw_lrwh_rectangle_textured(
            10 + 210,
            SCREEN_HEIGHT - 88,
            32,
            32,
            arcade.load_texture(":resources:images/items/coinGold.png")
        )

        # Рисуем сколько жизней осталось вверху экрана белым текстом
        arcade.draw_text(
            f"Жизней: {self.health}",
            10,
            SCREEN_HEIGHT - 30,
            arcade.csscolor.WHITE,
            18,
        )

    def hurt(self):
        self.health = max(0, self.health - 5)

        #arcade.play_sound(self.hurt_sound, volume=0.2)

        # Откидываем персонажа в сторону исходя из направления движения
        self.player_sprite.change_x = \
            -PLAYER_MOVEMENT_SPEED * 2 if self.player_sprite.change_x > 0 else PLAYER_MOVEMENT_SPEED * 2
        self.player_sprite.change_y = 5

        # Мигаем спрайтом красным цветом
        self.player_sprite.color = arcade.csscolor.RED
        arcade.schedule(lambda _: setattr(self.player_sprite, "color", arcade.csscolor.WHITE), 0.1)

    def center_player_camera(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.start_button.collides_with_point((x, y)):
            self.set_mouse_visible(False)
            self.paused = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.paused = not self.paused
            self.set_mouse_visible(True)
            return
        if self.paused:
            return
        # Механика прыжка и движения
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                #arcade.play_sound(self.jump_sound, volume=0.2)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if self.paused:
            return
        # Механика прыжка и движения
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def reset_level(self):
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 96

        self.scene["Coins"].clear()

        level.repopulate_tiles(self)

        self.health = 20

    def on_update(self, delta_time):
        self.last_score = self.scores[-1] if self.scores else 0
        self.best_score = max(self.scores) if self.scores else 0

        if self.paused:
            return

        self.current_player_animation.update()

        # Запрещаем двигаться влево за границу карты
        if self.player_sprite.center_x < 0:
            self.player_sprite.center_x = 0

        if self.health == 0:
            if self.current_player_animation.is_finished():
                self.reset_level()
            return

        # Анимация простоя
        if self.player_sprite.change_x == 0 and self.player_sprite.change_y == 0:
            self.switch_animation(self.idle_sprites, 0.05)
        else:
            self.switch_animation(self.walk_sprites, 0.1)

        # Обновляем физику
        self.physics_engine.update()

        # Проверяем столкновения
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        bomb_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Bombs"])

        if len(bomb_hit_list) > 0:
            # Мы попали в бомбу, отнимаем жизнь
            self.hurt()

            if self.health == 0:
                # arcade.play_sound(self.death_sound, volume=0.2)
                self.switch_animation(self.death_sprites, 0.1, False)
                self.scores.append(self.score)
                scores.save_scores(self.scores)
            return

        # Проверяем, собрали ли мы все монеты
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            #arcade.play_sound(self.collect_coin_sound, volume=0.2)
            self.score += 1

        if len(self.scene["Coins"]) == 0:
            #arcade.play_sound(self.win_sound, volume=0.2)
            self.reset_level()

        self.center_player_camera()
