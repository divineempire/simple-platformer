class SpriteAnimation:

    def __init__(self, sprite, textures, delay=0.1, loop=True):
        self.sprite = sprite
        self.textures = textures
        self.delay = delay
        self.frame = 0
        self.frame_timer = 0
        self.loop = loop
        self.end = False

    def is_finished(self):
        return self.end

    def update(self):
        if self.end:
            return

        self.frame += self.delay

        if self.frame >= len(self.textures):
            if self.loop:
                self.frame = 0
            else:
                self.frame = len(self.textures) - 1
                self.end = True

        self.sprite.texture = self.textures[int(self.frame)]
