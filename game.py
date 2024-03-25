import pygame as pg

def main():
    # Code to run the game here
    pg.init()

    clock = pg.time.Clock()
    width, height = 1200, 900 # map size 800x800, tiles are 56x56
    window = pg.display.set_mode((width, height))

    running = True
    while running:
        clock.tick(60) # 60 FPS

        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        window.fill((0, 0, 0))
        pg.display.flip()

    pg.quit()

if __name__ == '__main__':
    main()