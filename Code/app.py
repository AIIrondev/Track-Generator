import pygame as pg
import sys


# main function
def main():
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption('Hello World')
    clock = pg.time.Clock()
    bg_color = pg.Color('gray12')
    font = pg.font.Font(None, 64)
    text = font.render('Hello World', True, pg.Color('dodgerblue'))
    text_rect = text.get_rect(center=screen.get_rect().center)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.fill(bg_color)
        screen.blit(text, text_rect)
        pg.display.flip()
        clock.tick(30)
    
    
    
if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()