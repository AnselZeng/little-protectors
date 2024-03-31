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
        self.rect.center = (self.tileToPixel(tile))
        self.lastUpdate = pg.time.get_ticks()

    def tileToPixel(self, tile):
        return (tile[0] + 0.5) * c.TILE_SIZE, (tile[1] + 0.5) * c.TILE_SIZE
    def pixelToTile(self, pixel):
        return int(pixel[0] / c.TILE_SIZE - .5), int(pixel[1] / c.TILE_SIZE - .5)

    def move(self, path):
        for tileX, tileY in path:
            target = self.tileToPixel((tileX, tileY))
            while self.rect.center != target:
                self.rect.center = self.moveStep(target)
                yield

    def update(self):
        self.image = self.animationList[self.frameIndex]
        # check if enough time has passed since the last update
        if pg.time.get_ticks() - self.lastUpdate > 100:
            self.lastUpdate = pg.time.get_ticks()
            self.frameIndex = (self.frameIndex + 1) % len(self.animationList)