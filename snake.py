import pygame
import sys
import os
from pygame import Surface
from random import randrange
from collections import deque
SNAKE_SPEED = 65


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
    return sheet[0].subsurface((w * cords[0], h * cords[1], w, h))


def to_binary(f, s) -> int:
    n = f * 2 + s
    if n > 0:
        n = 3 - n
    return n


class Board:
    def __init__(self, x, y, width, height, plan, direction):
        self.field_w = len(plan[0])
        self.field_h = len(plan)
        self.cell_w = width // self.field_w
        self.cell_h = height // self.field_h
        self.x = x
        self.y = y
        self.plan = plan
        self.snake = pygame.sprite.Group()
        self.snake_body = pygame.sprite.Group()
        self.snake_head = pygame.sprite.Group()
        self.tileset = (load_image('master-tileset.png'), 10, 5)
        self.apple = pygame.transform.scale(cut_sheet((load_image('snake-graphics.png'), 5, 4), (0, 3)),
                                            (self.cell_w, self.cell_h))
        self.time = 0
        self.distance = 0
        self.dir_x = 0
        self.dir_y = 0
        self.nowdir_x = 0
        self.nowdir_y = 0
        self.snake_len = 0
        self.head_x = 0
        self.head_y = 0
        chords = []
        for i in range(len(plan)):
            for j in range(len(plan[i])):
                cur = plan[i][j]
                if cur.isdigit():
                    if len(chords) <= int(cur):
                        chords += [(0, 0)] * (int(cur) - len(chords) + 1)
                    chords[int(cur)] = (j, i)
        self.new_snake(chords, direction)
        for i in self.plan:
            print(i)

    def new_snake(self, chords, direction):
        if chords:
            self.time = 0
            self.distance = 0
            self.dir_x = direction[0]
            self.dir_y = direction[1]
            self.nowdir_x = direction[0]
            self.nowdir_y = direction[1]
            self.snake_len = len(chords)
            self.head_x = chords[0][0]
            self.head_y = chords[0][1]
            x = self.x + self.head_x * self.cell_w
            y = self.y + self.head_y * self.cell_h
            Head(x, y, self.cell_h, self.cell_w, direction, self.snake, self.snake_head)
            self.plan[chords[0][1]][chords[0][0]] = '0'
            act = []
            for i in range(1, len(chords)):
                x = self.x + chords[i][0] * self.cell_w
                y = self.y + chords[i][1] * self.cell_h
                self.plan[chords[i][1]][chords[i][0]] = str(i)
                act.append((chords[i - 1][0] - chords[i][0], chords[i - 1][1] - chords[i][1]))
                SnakePiece(x, y, self.cell_h, self.cell_w, direction, list(reversed(act)), self.snake, self.snake_body)

    def snake_control(self, time, x, y, screen):
        if self.snake_len == 0:
            return False
        time += self.time
        pixels = time / 1000 * SNAKE_SPEED
        move = int(pixels)
        ost = pixels - move
        self.time = ost * 1000 / SNAKE_SPEED
        self.distance += move
        if not x + self.dir_x == y + self.dir_y == 0 and (x != self.dir_x or y != self.dir_y) and abs(x + y) == 1:
            self.dir_x = x
            self.dir_y = y
        if self.distance >= self.cell_w:
            self.distance -= self.cell_w
            self.snake.update(move=move - self.distance)
            self.snake.update(change=True, x=self.dir_x, y=self.dir_y)
            self.head_x += self.nowdir_x
            self.head_y += self.nowdir_y
            eat = False
            if self.plan[self.head_y][self.head_x] == '@':
                eat = True
            for i in range(len(self.plan)):
                for j in range(len(self.plan[i])):
                    if self.plan[i][j].isdigit():
                        if int(self.plan[i][j]) + 1 == self.snake_len:
                            self.plan[i][j] = '.'
                        else:
                            self.plan[i][j] = str(int(self.plan[i][j]) + 1)
            self.plan[self.head_y][self.head_x] = '0'
            hx = self.head_x + self.dir_x
            hy = self.head_y + self.dir_y
            self.nowdir_x = self.dir_x
            self.nowdir_y = self.dir_y
            print()
            for i in self.plan:
                print(i)
            if 0 > hx or hx >= self.field_w or 0 > hy or hy >= self.field_h or self.plan[hy][hx] in ['#', '%']\
                    or self.plan[hy][hx].isdigit():
                self.snake_len = 0
                self.snake.update(die=True)
                self.snake.empty()
                self.snake_body.empty()
                self.snake_head.empty()
                for i in range(len(self.plan)):
                    for j in range(len(self.plan[i])):
                        if self.plan[i][j].isdigit():
                            self.plan[i][j] = '%'
                self.render(screen)
                return False
            else:
                if eat:
                    self.snake_len += 1
                    x = self.x + self.head_x * self.cell_w
                    y = self.y + self.head_y * self.cell_h
                    self.snake_body.update(sleep=True)
                    SnakePiece(x, y, self.cell_h, self.cell_w, (self.nowdir_x, self.nowdir_y),
                               [(0, 0)], self.snake, self.snake_body)
                self.snake.update(move=self.distance)
        elif move > 0:
            self.snake.update(move=move)
            self.render(screen)
        return True

    def render(self, screen: Surface):
        screen.fill('white')
        for i in range(self.field_h):
            for j in range(self.field_w):
                x = self.x + j * self.cell_w
                y = self.y + i * self.cell_h
                cur = self.plan[i][j]
                im = pygame.Surface((self.cell_w, self.cell_h))
                if cur == '%':
                    im.fill('gray')
                elif cur != '#':
                    im = pygame.transform.scale(cut_sheet(self.tileset, (0, 2)), (self.cell_w, self.cell_h))
                screen.blit(im, (x, y))
                if cur == '@':
                    screen.blit(self.apple, (x, y))
        self.snake_body.draw(screen)
        self.snake_head.draw(screen)

    def summon_apple(self):
        x = randrange(self.field_w)
        y = randrange(self.field_h)
        while self.plan[y][x] != '.':
            x = randrange(self.field_w)
            y = randrange(self.field_h)
        self.plan[y][x] = '@'


class SnakePiece(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, direction, acts, *group: pygame.sprite.Group) -> None:
        super().__init__(*group)
        self.image = pygame.Surface((width, height))
        self.image.fill("green")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dir_x = 0
        self.dir_y = 0
        self.order = deque(acts + [direction])
        self.change_dir(direction[0], direction[1])

    def update(self, change=False, x=0, y=0, move=0, die=False, sleep=False) -> None:
        if change:
            if x != y:
                self.change_dir(x, y)
            self.order.append((self.dir_x, self.dir_y))
            self.order.popleft()
        elif move != 0:
            act = self.order[0]
            self.rect = self.rect.move(move * act[0], move * act[1])
        elif sleep:
            self.order.appendleft((0, 0))
        elif die:
            im = pygame.Surface([self.rect.width, self.rect.height])
            im.fill(pygame.Color("gray"))
            self.image = im

    def change_dir(self, x, y):
        f = to_binary(self.order[0][0], self.order[0][1])
        s = to_binary(x, y)
        if f != s:
            ang = -90
            if f > s and not (f == 2 and s == -2) or f == -2 and s == 2:
                ang = 90
            self.image = pygame.transform.rotate(self.image, ang)
        self.dir_x = x
        self.dir_y = y


class Head(SnakePiece):
    def __init__(self, x: int, y: int, width: int, height: int, direction, *group: pygame.sprite.Group):
        super().__init__(x, y, width, height, direction, [], *group)
        self.draw_yourself()

    def draw_yourself(self):
        short = (self.rect.w + 1) // 5
        long = (self.rect.w + 1) // 5 * 3
        first = [short, long, short, short]
        second = [long, short, short, short]
        if self.dir_x == -1:
            second[0] = short
        elif self.dir_x == 1:
            first[0] = long
        elif self.dir_y == -1:
            first[1] = short
        elif self.dir_y == 1:
            second[1] = long
        self.image.fill('black', first)
        self.image.fill('black', second)


pygame.init()
WIDTH, HEIGHT = 765, 700
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
    board = Board(25, 25, 715, 650, plan, (1, 0))
    x = y = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pr = pygame.key.get_pressed()
                x = pr[pygame.K_d] - pr[pygame.K_a]
                y = pr[pygame.K_s] - pr[pygame.K_w]
        if not board.snake_control(clock.tick(50), x, y, screen):
            xc = randrange(0, board.field_w)
            board.new_snake([(xc, 2), (xc, 1), (xc, 0)], (0, 1))
            x = y = 0
        if randrange(100) < 1:
            board.summon_apple()
        pygame.display.flip()


if __name__ == '__main__':
    pygame.display.set_caption('Змейка')
    game()
    pygame.quit()
