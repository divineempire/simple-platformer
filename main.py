import arcade

from game import PlatformerGame


def main():
    window = PlatformerGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()