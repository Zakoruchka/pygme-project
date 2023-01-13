import pygame
import sys
import os
from pygame import Surface, draw
from random import randint


def load_image(name: str, colorkey=-1) -> Surface:
    """
    load_image(name, colorkey) -> Surface
    """
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey != -1:
        image = image.convert()
        if colorkey == 0:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def cut_sheet(sheet: Surface, columns, rows, x, y):
    w = sheet.get_width() // columns
    h = sheet.get_height() // rows
    return sheet.subsurface(pygame.Rect(w * x, h * y, w, h))


class Board:
    def __init__(self, x, y, width, height, plan):
        self.field_w = len(plan[0])
        self.field_h = len(plan)
        self.cell_w = width // self.field_w
        self.cell_h = height // self.field_h
        self.plan = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprites = pygame.sprite.Group()
        tileset = load_image('master-tileset.png')
        for i in range(len(plan)):
            plan.append([])
            for j in range(len(plan[i])):
                im = cut_sheet(tileset, 10, 5, randint(0, 7), 2)
                plan.append(Tile(im, self.x + j * self.cell_h, self.y + i * self.cell_w, self.sprites))

    def render(self, screen: Surface):
        self.sprites.draw(screen)
        # for i in range(len(self.plan)):
        #     for j in range(len(self.plan[i])):
        #         rect = (self.x + self.cell_w * j, self.y + self.cell_h * i, self.cell_w, self.cell_h)
        #         draw.rect(screen, 'black', rect, 1)


class Tile(pygame.sprite.Sprite):
    def __init__(self, image_file_name: Surface, x: int, y: int, group: pygame.sprite.Group) -> None:
        super().__init__(group)
        self.image = image_file_name
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


pygame.init()
WIDTH, HEIGHT = 700, 700
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def game():
    running = True
    tileset = cut_sheet(load_image('master-tileset.png'), 10, 5, 3, 2)
    group = pygame.sprite.Group()
    board = Board(25, 25, 650, 650, [['.'] * 10 for i in range(10)])
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(FPS)
        screen.fill('white')
        board.render(screen)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.display.set_caption('Змейка')
    game()
    pygame.quit()
