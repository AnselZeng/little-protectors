import pygame as pg
import src.notInterface.constants as c
import math
from src.gameData import (TOWER_DATA)
import heapq

class Turret(pg.sprite.Sprite):
    def __init__(self, type, spriteSheets, tile):
        pg.sprite.Sprite.__init__(self)
        self.range = TOWER_DATA[type]["range"] * c.TILE_SIZE
        self.cooldown = TOWER_DATA[type]["cooldown"]
        self.cost = TOWER_DATA[type]["cost"]
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None
        self.type = type
        self.damage = TOWER_DATA[type]["damage"]
        self.upgraded = [False, False, False] # upgrade levels

        # position variables
        self.tile_x = tile[0]
        self.tile_y = tile[1]
        # calculate center coordinates
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE

        # animation variables
        self.sprite_sheet = spriteSheets[type]
        self.animation_list = self.load_images()
        self.frame_index = len(self.animation_list) - 1
        self.update_time = pg.time.get_ticks()

        # update image
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # create transparent circle showing range
        self.range_circle = pg.Surface((self.range * 2, self.range * 2))
        self.range_circle.fill((0, 0, 0))
        self.range_circle.set_colorkey((0, 0, 0))
        pg.draw.circle(
            self.range_circle, "grey100", (self.range, self.range), self.range
        )
        self.range_circle.set_alpha(100)
        self.range_rect = self.range_circle.get_rect()
        self.range_rect.center = self.rect.center

    def load_images(self):
        # extract images from spritesheet
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(TOWER_DATA[self.type]["animation_steps"]):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, enemy_group):
        # if target picked, play firing animation
        if self.target:
            self.play_animation()
        else:
            # search for new target once turret has cooled down
            if pg.time.get_ticks() - self.last_shot > self.cooldown:
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        # find an enemy to target
        x_dist = 0
        y_dist = 0
        # check distance to each enemy to see if it is in range
        inRange = []
        for enemy in enemy_group:
            x_dist = enemy.pos[0] - self.x
            y_dist = enemy.pos[1] - self.y
            dist = math.sqrt(x_dist**2 + y_dist**2)
            if dist < self.range:
                inRange.append((dist, enemy))
        if inRange:
            self.target = sorted(inRange, key=lambda x: x[0])[0][1]

    def play_animation(self):
        # update image
        self.original_image = self.animation_list[self.frame_index]
        # check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > c.TR_ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
        # check if the animation has finished and reset to idle
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            
            # record completed time and clear target so cooldown can begin
            self.last_shot = pg.time.get_ticks()
            if self.target:
                self.target.takeDamage(self.damage)
            self.target = None

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_circle, self.range_rect)
