import pygame as pg
import json

# from enemy import Enemy
from src.interface.world import World
from src.interface.turret import Turret
from src.interface.button import Button
import src.notInterface.constants as c


# initialise pygame
pg.init()

# create clock
clock = pg.time.Clock()

# create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

# game variables
placing_turrets = False


# load images
# map
map_image = pg.image.load("assets/map/map.png").convert_alpha()
# turret spritesheets
turret_sheet = pg.image.load("assets/Archer/5.png").convert_alpha()
# individual turret image for mouse cursor
cursor_turret = pg.image.load("assets/Archer/36.png").convert_alpha()
# enemies
# enemy_image = pg.image.load("assets/images/enemies/enemy_1.png").convert_alpha()

# buttons
buy_turret_image = pg.image.load("assets/buttons/buy_turret.png").convert_alpha()
cancel_image = pg.image.load("assets/buttons/cancel.png").convert_alpha()
debug_image = pg.image.load("assets/buttons/debug.png").convert_alpha()

# load json data for level
# with open("levels/level.tmj") as file:
#     world_data = json.load(file)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    mouseTile = (mouse_tile_x, mouse_tile_y)
    # calculate the sequential number of the tile
    # mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    # if world.tile_map[mouse_tile_num] == 7:

    # check if that tile is grass
    if mouseTile in pathTiles:
        print("Can't place turret on path")
        return
    
    # check that there isn't already a turret there
    for turret in turret_group:
        if mouseTile == (turret.tile_x, turret.tile_y):
            print("Turret already there")
            return
    # if it is a free space then create turret
    new_turret = Turret(turret_sheet, mouse_tile_x, mouse_tile_y)
    turret_group.add(new_turret)


# create world
world = World(map_image)
# initialise path data
pathTiles = [
    [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2],
    [5, 3],
    [5, 4], 
    [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5], [9, 5],
    [5, 6], [9, 6],
    [5, 7], [9, 7],
    [5, 8], [9, 8],
    [5, 9], [6, 9], [7, 9], [8, 9], [9, 9], [12, 9], [13, 9], [14, 9],
    [9, 10],[12, 10],
    [9, 11],[12, 11],
    [9, 12],[10, 12],[11, 12],[12, 12],
]
pathTiles = list(map(lambda x: (x[0], x[1]), pathTiles))

# world.process_data()

# create groups
# enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# enemy = Enemy(world.waypoints, enemy_image)
# enemy_group.add(enemy)

# create buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
debug_button = Button(c.SCREEN_WIDTH + 50, 240, debug_image, True)

# game loop
run = True
while run:

    clock.tick(c.FPS)

    #########################
    # UPDATING SECTION
    #########################

    # update groups
    # enemy_group.update()
    turret_group.update()

    #########################
    # DRAWING SECTION
    #########################

    screen.fill("grey100")

    # draw level
    world.draw(screen)

    # draw groups
    # enemy_group.draw(screen)
    turret_group.draw(screen)

    # draw buttons
    # debug button for testing
    if debug_button.draw(screen):
        print("Debug button pressed")
        print("Turret group:")
        for turret in turret_group:
            print(turret.tile_x, turret.tile_y)

    # button for placing turrets
    if turret_button.draw(screen):
        placing_turrets = True
    
    # if placing turrets then show the cancel button as well
    if placing_turrets == True:
        # show cursor turret
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= c.SCREEN_WIDTH:
            screen.blit(cursor_turret, cursor_rect)
        if cancel_button.draw(screen):
            placing_turrets = False

    # event handler
    for event in pg.event.get():
        # quit program
        if event.type == pg.QUIT:
            run = False
        # mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()

            # check if mouse is on the game area
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                if placing_turrets == True:
                    create_turret(mouse_pos)

    # update display
    pg.display.flip()

pg.quit()
