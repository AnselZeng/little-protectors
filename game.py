import pygame as pg
import json

# from enemy import Enemy
from src.interface.world import World
from src.interface.turret import Turret
from src.interface.button import Button
from src.notInterface.enemy import Enemy
import src.notInterface.constants as c
from src.gameData import (ROUNDS)

class Game:
    def __init__(self):

        # Initialise pygame
        pg.init()

        # Create clock
        self.clock = pg.time.Clock()

        # Create game window
        self.screen = pg.display.set_mode(
            (c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT)
        )
        pg.display.set_caption("Little Defenders")

        self.load_images()

        # Game State
        self.placingTurrets = False

        # Create world
        self.world = World(self.mapImage)

        # initialise path data
        self.pathTiles = [
            (0, 2),
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
            (5, 3),
            (5, 4),
            (0, 5),
            (1, 5),
            (2, 5),
            (3, 5),
            (4, 5),
            (5, 5),
            (6, 5),
            (7, 5),
            (8, 5),
            (9, 5),
            (5, 6),
            (9, 6),
            (5, 7),
            (9, 7),
            (5, 8),
            (9, 8),
            (5, 9),
            (6, 9),
            (7, 9),
            (8, 9),
            (9, 9),
            (12, 9),
            (13, 9),
            (14, 9),
            (9, 10),
            (12, 10),
            (9, 11),
            (12, 11),
            (9, 12),
            (10, 12),
            (11, 12),
            (12, 12),
        ]

        self.path1 = [
            (0, 2),
            (5, 2),
            (5, 9),
            (9, 9),
            (9, 12),
            (12, 12),
            (12, 9),
            (14, 9),
        ]
        self.path2 = [
            (0, 5),
            (9, 5),
            (9, 12),
            (12, 12),
            (12, 9),
            (14, 9),
        ]

        # Create groups
        self.enemyGroup = pg.sprite.Group()
        self.turretGroup = pg.sprite.Group()

        # game variables
        self.selected_turret = None

        # game variables
        self.selected_turret = None

        # Initialize rounds
        self.currentRound = 0
        self.roundInProgress = False
        self.spawningEnemies = False
        self.lastSpawn = pg.time.get_ticks()
        self.nextRound()

        # Text display
        self.textFont = pg.font.SysFont("consolas", 24)

        # Create buttons
        self.archerButton = Button(c.SCREEN_WIDTH + 5, 70, self.archerButtonImage, True)
        self.knightButton = Button(c.SCREEN_WIDTH + 105, 70, self.knightButtonImage, True)
        self.fighterButton = Button(c.SCREEN_WIDTH + 205, 70, self.fighterButtonImage, True)
        self.cancelButton = Button(c.SCREEN_WIDTH + 15, 750, self.cancelButtonImage, True)
        self.nextRoundButton = Button(c.SCREEN_WIDTH -80, 750, self.nextRoundButtonImage, True)
        self.sellButton = Button(c.SCREEN_WIDTH + 15, 750, self.sellButtonImage, True)

        # Initialize resources
        self.gold = 100
    
    # Draw text
    def drawText(self, text, font, colour, x, y):
        img = font.render(text, True, colour)
        self.screen.blit(img, (x, y))

    # Spawn enemies
    def spawnEnemies(self):
        if not (self.spawnList1 or self.spawnList2): # If there are no more enemies to spawn
            self.spawningEnemies = False
            self.currentRound += 1
            self.nextRound()
            return
        if self.spawnList1: # If there are enemies to spawn on path 1
            enemyType = self.spawnList1.pop()
            self.enemyGroup.add(Enemy(enemyType, self.enemySheets, self.path1))
        if self.spawnList2: # If there are enemies to spawn on path 2
            enemyType = self.spawnList2.pop()
            self.enemyGroup.add(Enemy(enemyType, self.enemySheets, self.path2))

    # Load the next round of enemies
    def nextRound(self): 
        if self.currentRound == len(ROUNDS):
            print("Game over")
            return
        enemyP1, enemyP2 = ROUNDS[self.currentRound]
        self.spawnList1 = []
        self.spawnList2 = []
        for enemyType in enemyP1:
            for _ in range(enemyP1[enemyType]):
                self.spawnList1.append(enemyType)
            for _ in range(enemyP2[enemyType]):
                self.spawnList2.append(enemyType)
        print(f"Round {self.currentRound + 1}/{len(ROUNDS)}")
        print(self.spawnList1)
        print(self.spawnList2)

    # Load images
    def load_images(self):
        # Map
        self.mapImage = pg.image.load("assets/map/map.png").convert_alpha()

        # Turret spritesheets
        self.turretSheets = {
            "archer": pg.image.load("assets/archer/archer_shoot.png").convert_alpha(),
            "knight": pg.image.load("assets/knight/knight_swing.png").convert_alpha(),
            "fighter": pg.image.load("assets/fighter/fighter_swing.png").convert_alpha(),
        }

        self.turretStatics = {
            "archer": pg.image.load("assets/archer/archer_static.png").convert_alpha(),
            "knight": pg.image.load("assets/knight/knight_static.png").convert_alpha(),
            "fighter": pg.image.load("assets/fighter/fighter_static.png").convert_alpha(),
        }
        
        # Enemy spritesheets
        self.enemySheets = {
            "rg": pg.image.load("assets/enemies/red_goblin_walk.png").convert_alpha(),
            "bg": pg.image.load("assets/enemies/blue_goblin_walk.png").convert_alpha(),
            "yg": pg.image.load("assets/enemies/yellow_goblin_walk.png").convert_alpha(),
            "pg": pg.image.load("assets/enemies/purple_goblin_walk.png").convert_alpha(),
            "tg": pg.image.load("assets/enemies/tnt_goblin_walk.png").convert_alpha()
        }

        # Buttons
        # Turret buttons
        self.archerButtonImage= pg.image.load("assets/protectors/archer1.png").convert_alpha()
        self.archerButtonImageFaded = pg.image.load("assets/protectors/archer2.png").convert_alpha()
        self.knightButtonImage = pg.image.load("assets/protectors/knight1.png").convert_alpha()
        self.knightButtonImageFaded = pg.image.load("assets/protectors/knight2.png").convert_alpha()
        self.fighterButtonImage = pg.image.load("assets/protectors/fighter1.png").convert_alpha()
        self.fighterButtonImageFaded = pg.image.load("assets/protectors/fighter2.png").convert_alpha()

        self.cancelButtonImage = pg.image.load("assets/buttons/cancel_icon.png").convert_alpha()
        self.nextRoundButtonImage = pg.image.load("assets/buttons/play.png").convert_alpha()
        self.sellButtonImage = pg.image.load("assets/buttons/sell.png").convert_alpha()

    def create_turret(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        mouseTile = (mouse_tile_x, mouse_tile_y)

        # check if that tile is grass
        if mouseTile in self.pathTiles:
            print("Can't place turret on path")
            return

        # check that there isn't already a turret there
        for turret in self.turretGroup:
            if mouseTile == (turret.tile_x, turret.tile_y):
                print("Turret already there")
                return

        # if it is a free space then create turret
        self.turretGroup.add(Turret(self.turretType, self.turretSheets, mouseTile))
        print(f"{self.turretType} turret created @ {mouseTile}")

    def select_turret(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        for turret in self.turretGroup:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                return turret

    def clear_selection(self):
        for turret in self.turretGroup:
            turret.selected = False

    def run(self):
        # game loop
        run = True
        while run:

            self.clock.tick(c.FPS)

            #########################
            # UPDATING SECTION
            #########################

            # Update groups
            self.enemyGroup.update()
            self.turretGroup.update(self.enemyGroup)

            # highlight selected turret
            if self.selected_turret:
                self.selected_turret.selected = True

            #########################
            # DRAWING SECTION
            #########################

            # Draw background
            self.screen.fill((255, 255, 255))  # Fill with white color as a fallback
            background = pg.image.load("assets/map/bg.png")  # Load background image
            self.screen.blit(background, (0, 0))  # Blit background image at (0, 0)

            # Draw level
            self.world.draw(self.screen)

            # Draw groups
            self.enemyGroup.draw(self.screen)
            for turret in self.turretGroup:
                turret.draw(self.screen)

            for turret in self.turretGroup:
                if turret.target:
                    pg.draw.line(self.screen, "red", turret.rect.center, turret.target.pos, 2)

            # Draw buttons
            # Next round button
            if len(self.enemyGroup) == 0:
                if self.nextRoundButton.draw(self.screen):
                    self.roundInProgress = True
                    self.spawningEnemies = True

            # Enter turret placement mode
            if self.archerButton.draw(self.screen):
                self.placingTurrets = True
                self.turretType = "archer"
            if self.knightButton.draw(self.screen):
                self.placingTurrets = True
                self.turretType = "knight"
            if self.fighterButton.draw(self.screen):
                self.placingTurrets = True
                self.turretType = "fighter"
            

            self.drawText(f"Gold: {self.gold}", self.textFont, "black", 30, 30)

            for enemy in self.enemyGroup:
                pg.draw.rect(enemy.image, (255, 0, 0), (enemy.pos[0], enemy.pos[1], 50, 5))
                pg.draw.rect(enemy.image, (0, 255, 0), (enemy.pos[0], enemy.pos[1], 50 * (enemy.hp / enemy.maxHp), 5))

            # Sell button should only be visible when a turret is selected
            if self.selected_turret:
                if self.sellButton.draw(self.screen):
                    self.turretGroup.remove(self.selected_turret)
                    self.gold += self.selected_turret.cost // 2
                    self.selected_turret = None

            # If placing turrets then show the cancel button as well
            if self.placingTurrets:
                # Show turret image at mouse position
                cursor_rect = self.turretStatics[self.turretType].get_rect()
                cursor_pos = pg.mouse.get_pos()
                cursor_rect.center = cursor_pos

                if cursor_pos[0] <= c.SCREEN_WIDTH:
                    self.screen.blit(self.turretStatics[self.turretType], cursor_rect)

                # Exit placement mode if cancel button is pressed
                if self.cancelButton.draw(self.screen):
                    self.placingTurrets = False

            # Spawn enemies
            if self.spawningEnemies:
                if pg.time.get_ticks() - self.lastSpawn > c.SPAWN_RATE:
                    self.spawnEnemies()
                    self.lastSpawn = pg.time.get_ticks()

            # Event handler
            for event in pg.event.get():
                # Quit program
                if event.type == pg.QUIT:
                    run = False                      

                # Mouse click
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pg.mouse.get_pos()

                    # Check if mouse is on the game area
                    if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                        # clear selected turrets
                        self.selected_turret = None
                        self.clear_selection()
                        if self.placingTurrets == True:
                            self.create_turret(mouse_pos)
                        else:
                            self.selected_turret = self.select_turret(mouse_pos)

            # update display
            pg.display.flip()

        pg.quit()
