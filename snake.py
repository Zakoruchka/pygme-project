import pygame
import sys
import os
from pygame import Surface
from random import randrange
from collections import deque
SYMBOLS_SPRITE_CORDS = {'/\\': (3, 0), '>': (4, 0), '\\/': (4, 1), '<': (3, 1), '|': (2, 1), '-': (1, 0), '/>': (0, 0),
                        '</': (2, 2), '\\>': (0, 1), '<\\': (2, 0), '-/\\': (3, 2), '->': (4, 2), '-\\/': (4, 3), '<-':
                        (3, 3)}
SYMBOLS_DIRS = {'/\\': (0, -1), '>': (1, 0), '\\/': (0, 1), '<': (-1, 0), '-/\\': (0, -1), '->': (1, 0),
                '-\\/': (0, 1), '<-': (-1, 0)}


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


def cut_sheet(sheet: tuple[Surface, int, int], cords: tuple[int, int]) -> Surface:
    """
    load_image(sheet, cords) -> Surface
    """
    w = sheet[0].get_width() // sheet[1]
    h = sheet[0].get_height() // sheet[2]
    return sheet[0].subsurface(pygame.Rect(w * cords[0], h * cords[1], w, h))


class Board:
    def __init__(self, x, y, width, height, plan):
        self.field_w = len(plan[0])
        self.field_h = len(plan)
        self.cell_w = width // self.field_w
        self.cell_h = height // self.field_h
        self.plan = []
        self.x = x
        self.y = y
        self.sprites = pygame.sprite.Group()
        self.snake = pygame.sprite.Group()
        tileset = (load_image('master-tileset.png'), 10, 5)
        snakeset = (load_image('snake-graphics.png'), 5, 4)
        for i in range(len(plan)):
            self.plan.append([])
            for j in range(len(plan[i])):
                tile_im = cut_sheet(tileset, (randrange(0, 8, 2), 2))
                x = self.x + j * self.cell_w
                y = self.y + i * self.cell_h
                cur = plan[i][j]
                if cur in ['.', '@']:
                    self.plan[-1].append(Tile(tile_im, x, y, self.cell_h, self.cell_w, '.', self.sprites))
                else:
                    Tile(tile_im, x, y, self.cell_h, self.cell_w, '.', self.sprites)
                    if cur == '@':
                        im = cut_sheet(snakeset, (0, 3))
                        self.plan[-1].append(Tile(im, x, y, self.cell_h, self.cell_w, '@', self.sprites))
                    else:
                        im = cut_sheet(snakeset, SYMBOLS_SPRITE_CORDS[plan[i][j]])
                        self.plan[-1].append(SnakePiece(im, x, y, self.cell_h, self.cell_w, plan[i][j], self.snake,
                                                        dirs=SYMBOLS_DIRS[cur]))
                        if cur in ['-/\\', '<-', '-\\/', '->']:
                            self.plan[-1][-1].order.append(SYMBOLS_DIRS[cur])

    def render(self, screen: Surface):
        self.sprites.draw(screen)
        self.snake.draw(screen)

    def manage_dir(self, x, y):
        self.snake.update(change=True, x=x, y=y)

    def move_snake(self, s):
        self.snake.update(move=s)


class Tile(pygame.sprite.Sprite):
    def __init__(self, image: Surface, x: int, y: int, width: int, height: int, type: str, *group: pygame.sprite.Group)\
            -> None:
        super().__init__(*group)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type


class SnakePiece(Tile):
    def __init__(self, image: Surface, x: int, y: int, width: int, height: int, *group: pygame.sprite.Group,
                 dirs=(0, 0)) -> None:
        super().__init__(image, x, y, width, height, *group)
        self.dir_x = dirs[0]
        self.dir_y = dirs[1]
        self.order = deque([(dirs[0], dirs[1])])

    def update(self, change=False, move=0, x=0, y=0) -> None:
        if change:
            if x != y:
                self.dir_x = x
                self.dir_y = y
            self.order.append((self.dir_x, self.dir_y))
            self.order.popleft()
        if move != 0:
            act = self.order[0]
            self.rect = self.rect.move(move * act[0], move * act[1])


pygame.init()
WIDTH, HEIGHT = 700, 700
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


def game():
    running = True
    plan = [i.split() for i in open('data/snake_plan.txt', encoding="utf-8").read().split('\n')]
    board = Board(25, 25, 650, 650, plan)
    x = y = 0
    secs = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pr = pygame.key.get_pressed()
                x = pr[pygame.K_RIGHT] - pr[pygame.K_LEFT]
                y = pr[pygame.K_DOWN] - pr[pygame.K_UP]
        tick = clock.tick(200)
        secs += tick
        if secs / 1000 * 200 >= board.cell_w:
            secs -= board.cell_w / 200 * 1000
            board.manage_dir(x, y)
        screen.fill('white')
        board.render(screen)
        board.move_snake(tick / 1000 * 200)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.display.set_caption('Змейка')
    game()
    pygame.quit()
