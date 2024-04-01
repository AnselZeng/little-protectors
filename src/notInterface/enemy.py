import pygame as pg
from pygame.math import Vector2
import src.notInterface.constants as c
from src.gameData import (ENEMY_DATA)
class Enemy(pg.sprite.Sprite):
    def __init__(self, parent, type, spriteSheets, waypoints, frames = 6) -> None:
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)

        # Set parent
        self.parent = parent

        # Health
        self.maxHp = ENEMY_DATA[type]["hp"]
        self.hp = ENEMY_DATA[type]["hp"]
        self.speed = ENEMY_DATA[type]["speed"]
        
        # Animation variables
        size = spriteSheets[type].get_height()
        self.animationList = [spriteSheets[type].subsurface(x * size, 0, size, size) for x in range(frames)]

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

    def tileToPixel(self, tile):
        return ((tile[0] + 0.5) * c.TILE_SIZE, (tile[1] + 0.5) * c.TILE_SIZE)
    
    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

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
                self.parent.health -= 1
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