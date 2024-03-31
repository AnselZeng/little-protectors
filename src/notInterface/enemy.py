import pygame as pg
import src.notInterface.constants as c

class Enemy(pg.sprite.Sprite):
    def __init__(self, spriteSheet, frames, tile) -> None:
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)
        # Animation variables
        size = spriteSheet.get_height()
        self.animationList = [spriteSheet.subsurface(x * size, 0, size, size) for x in range(frames)]

        # Set animation variables
        self.frames = frames
        self.frameIndex = 0

        # Update image
        self.image = self.animationList[self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = ((tile[0] + 0.5) * c.TILE_SIZE, (tile[1] + 0.5) * c.TILE_SIZE)
        self.lastUpdate = pg.time.get_ticks()

    def move(self, dx, dy):
        for _ in range(dx * c.TILE_SIZE):
            self.rect.x += 1
        for _ in range(dy * c.TILE_SIZE):
            self.rect.y += 1

    def update(self):
        self.image = self.animationList[self.frameIndex]
        # check if enough time has passed since the last update
        if pg.time.get_ticks() - self.lastUpdate > 100:
            self.lastUpdate = pg.time.get_ticks()
            self.frameIndex = (self.frameIndex + 1) % len(self.animationList)