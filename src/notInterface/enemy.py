import pygame as pg
from pygame.math import Vector2
import src.notInterface.constants as c

class Enemy(pg.sprite.Sprite):
    def __init__(self, spriteSheet, frames, waypoints) -> None:
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
        self.lastUpdate = pg.time.get_ticks()

        # Pathing'
        self.waypoints = waypoints
        self.pos = Vector2(self.tileToPixel(self.waypoints[0]))
        self.nextWaypoint = 1
        self.rect.center = (self.tileToPixel(self.pos))
        self.speed = 1



    def tileToPixel(self, tile):
        return ((tile[0] + 0.5) * c.TILE_SIZE, (tile[1] + 0.5) * c.TILE_SIZE)
    def pixelToTile(self, pixel):
        return (int(pixel[0] / c.TILE_SIZE - .5), int(pixel[1] / c.TILE_SIZE - .5))

    def move(self):
        self.target = Vector2(self.tileToPixel(self.waypoints[self.nextWaypoint]))
        self.movement = self.target - self.pos
        distance = self.movement.length()
        if distance < self.speed: # If the enemy is close enough to the next waypoint, move to the next waypoint
            # self.pos += self.movement.normalize() * distance
            self.nextWaypoint += 1
            if self.nextWaypoint >= len(self.waypoints):
                print("Enemy reached the end of the path")
                self.kill()
        else: # If the enemy is not close enough to the next waypoint, move towards it
            self.pos += self.movement.normalize() * self.speed
            
        self.rect.center = self.pos

    def update(self):
        self.move()
        self.image = self.animationList[self.frameIndex]
        # check if enough time has passed since the last update
        if pg.time.get_ticks() - self.lastUpdate > 100:
            self.lastUpdate = pg.time.get_ticks()
            self.frameIndex = (self.frameIndex + 1) % len(self.animationList)