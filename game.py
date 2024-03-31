import pygame as pg
import json

# from enemy import Enemy
from src.interface.world import World
from src.interface.turret import Turret
from src.interface.button import Button
from src.notInterface.enemy import Enemy
import src.notInterface.constants as c

class Game:
    def __init__(self):

        # Initialise pygame
        pg.init()

        # Create clock
        self.clock = pg.time.Clock()

        # Create game window
        self.screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
        pg.display.set_caption("Little Defenders")

        self.load_images()

        # Game State
        self.placingTurrets = False

        # Create world
        self.world = World(self.mapImage)

        # initialise path data
        self.pathTiles = [
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
            (5, 3),
            (5, 4), 
            (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
            (5, 6), (9, 6),
            (5, 7), (9, 7),
            (5, 8), (9, 8),
            (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (12, 9), (13, 9), (14, 9),
            (9, 10),(12, 10),
            (9, 11),(12, 11),
            (9, 12),(10, 12),(11, 12),(12, 12),
        ]

        self.path1 = [
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
            (5, 3),
            (5, 4),
            (5, 5),
            (5, 6),
            (5, 7),
            (5, 8),
            (5, 9), (6, 9), (7, 9), (8, 9), (9, 9),
            (9, 10),
            (9, 11),
            (9, 12), (10, 12), (11, 12), (12, 12),
            (12, 11), (12, 10), (12, 9), (13, 9), (14, 9),
        ]
        self.path2 = []

        # Create groups
        self.enemyGroup = pg.sprite.Group()
        self.turretGroup = pg.sprite.Group()

        # TEST
        self.enemyGroup.add(Enemy(self.enemySheet, 6, (5, 9)))

        # Create buttons
        self.turretButton = Button(c.SCREEN_WIDTH + 30, 120, self.turretButtonImage, True)
        self.cancelButton = Button(c.SCREEN_WIDTH + 50, 180, self.cancelButtonImage, True)
        self.debugButton = Button(c.SCREEN_WIDTH + 50, 240, self.debugButtonImage, True)

    # Load images
    def load_images(self):
        # Map
        self.mapImage = pg.image.load("assets/map/map.png").convert_alpha()

        # Turret spritesheets
        self.turretSheet = pg.image.load("assets/archer/archer_shoot.png").convert_alpha()
        self.turretStatic = pg.image.load("assets/archer/archer_static.png").convert_alpha()
        self.enemySheet = pg.image.load("assets/enemies/red_goblin_walk.png").convert_alpha()

        # Buttons
        self.turretButtonImage = pg.image.load("assets/buttons/buy_turret.png").convert_alpha()
        self.cancelButtonImage = pg.image.load("assets/buttons/cancel.png").convert_alpha()
        self.debugButtonImage = pg.image.load("assets/buttons/debug.png").convert_alpha()

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
        self.turretGroup.add(Turret(self.turretSheet, mouseTile))
    
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
            self.turretGroup.update()

            #########################
            # DRAWING SECTION
            #########################

            self.screen.fill("grey100")

            # Draw level
            self.world.draw(self.screen)

            # Draw groups
            self.enemyGroup.draw(self.screen)
            self.turretGroup.draw(self.screen)

            # Draw buttons
            # Debug button
            if self.debugButton.draw(self.screen):
                print("Debug button pressed")
                print("Turret group:")
                for turret in self.turretGroup:
                    print((turret.tile_x, turret.tile_y))

            # Enter turret placement mode
            if self.turretButton.draw(self.screen):
                self.placingTurrets = True
            
            # If placing turrets then show the cancel button as well
            if self.placingTurrets:
                # Show turret image at mouse position
                cursor_rect = self.turretStatic.get_rect()
                cursor_pos = pg.mouse.get_pos()
                cursor_rect.center = cursor_pos
                if cursor_pos[0] <= c.SCREEN_WIDTH:
                    self.screen.blit(self.turretStatic, cursor_rect)
                # Exit placement mode if cancel button is pressed
                if self.cancelButton.draw(self.screen):
                    self.placingTurrets = False

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
                        if self.placingTurrets == True:
                            self.create_turret(mouse_pos)

            # update display
            pg.display.flip()

        pg.quit()
