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
    def __init__(self, x, y, width, height, cell_w):
        self.field_w = width // cell_w
        self.field_h = height // cell_w
        self.cell_w = self.cell_h = cell_w
        self.x = x
        self.y = y
        self.plan = [['.'] * self.field_w for i in range(self.field_h)]
        self.snake = pygame.sprite.Group()
        self.snake_tail = pygame.sprite.Group()
        self.tileset = (load_image('master-tileset.png'), 10, 5)
        self.apple = pygame.transform.scale(cut_sheet((load_image('snake-graphics.png'), 5, 4), (0, 3)),
                                            (self.cell_w, self.cell_h))
        self.time = 0
        self.distance = 0
        self.dir_x = 0
        self.dir_y = 0
        self.snake_len = 0
        self.head = None
        self.tail = None

    def new_snake(self, chords, direction):
        if chords:
            self.time = 0
            self.distance = 0
            self.dir_x = direction[0]
            self.dir_y = direction[1]
            self.snake_len = len(chords)
            x = self.x + chords[0][0] * self.cell_w
            y = self.y + chords[0][1] * self.cell_h
            self.head = Head(x, y, self.cell_h, self.cell_w, direction, chords[0][0], chords[0][1],
                             self.snake)
            self.plan[chords[0][1]][chords[0][0]] = '>'
            self.plan[chords[-1][1]][chords[-1][0]] = '<'
            act = []
            for i in range(1, len(chords) - 1):
                self.plan[chords[i][1]][chords[i][0]] = '-'
                act.append((chords[i - 1][0] - chords[i][0], chords[i - 1][1] - chords[i][1]))
            x = self.x + chords[-1][0] * self.cell_w
            y = self.y + chords[-1][1] * self.cell_h
            act.append((chords[-2][0] - chords[-1][0], chords[-2][1] - chords[-1][1]))
            self.tail = Tail(x, y, self.cell_h, self.cell_w, direction, list(reversed(act)), chords[-1][0],
                             chords[-1][1], self.snake, self.snake_tail)

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
            self.plan[self.head.y][self.head.x] = '-'
            self.plan[self.tail.y][self.tail.x] = '.'
            self.snake.update(change=True, x=self.dir_x, y=self.dir_y)
            if self.plan[self.head.y][self.head.x] == '@':
                self.snake_len += 1
                self.snake_tail.update(sleep=True)
            self.plan[self.head.y][self.head.x] = '>'
            self.plan[self.tail.y][self.tail.x] = '<'
            hx = self.head.x + self.dir_x
            hy = self.head.y + self.dir_y
            print()
            for i in self.plan:
                print(i)
            if 0 > hx or hx >= self.field_w or 0 > hy or hy >= self.field_h or\
                    self.plan[hy][hx] in ['#', '%', '-', '<']:
                self.snake_len = 0
                self.snake.update(die=True)
                self.snake.empty()
                self.snake_tail.empty()
                for i in range(len(self.plan)):
                    for j in range(len(self.plan[i])):
                        if self.plan[i][j] in ['<', '-', '>']:
                            self.plan[i][j] = '%'
                self.render(screen)
                return False
            else:
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
                if cur in ['>', '-']:
                    im.fill('green')
                elif cur == '%':
                    im.fill('gray')
                elif cur != '#':
                    im = pygame.transform.scale(cut_sheet(self.tileset, (0, 2)), (self.cell_w, self.cell_h))
                screen.blit(im, (x, y))
                if cur == '@':
                    screen.blit(self.apple, (x, y))
        self.snake.draw(screen)

    def summon_apple(self):
        x = randrange(self.field_w)
        y = randrange(self.field_h)
        while self.plan[y][x] != '.':
            x = randrange(self.field_w)
            y = randrange(self.field_h)
        self.plan[y][x] = '@'


class Tail(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, direction, acts, x_pos, y_pos,
                 *group: pygame.sprite.Group) -> None:
        super().__init__(*group)
        self.image = pygame.Surface((width, height))
        self.image.fill("green")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dir_x = 0
        self.dir_y = 0
        self.x = x_pos
        self.y = y_pos
        self.order = deque(acts + [direction])
        self.draw_yourself()
        self.change_dir(direction[0], direction[1])

    def draw_yourself(self):
        pass

    def update(self, change=False, x=0, y=0, move=0, die=False, sleep=False) -> None:
        if change:
            if x != y:
                self.change_dir(x, y)
            self.order.append((self.dir_x, self.dir_y))
            self.x += self.order[0][0]
            self.y += self.order[0][1]
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


class Head(Tail):
    def __init__(self, x: int, y: int, width: int, height: int, direction, x_pos, y_pos, *group: pygame.sprite.Group):
        super().__init__(x, y, width, height, direction, [], x_pos, y_pos, *group)

    def draw_yourself(self):
        short = (self.rect.w + 1) // 5
        long = (self.rect.w + 1) // 5 * 3
        first = [short, long, short, short]
        second = [long, long, short, short]
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
    board = Board(25, 25, 715, 650, 65)
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
