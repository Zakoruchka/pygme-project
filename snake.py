import pygame
import sys
import os
from pygame import Surface
from random import randrange
from collections import deque


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
        self.eaten = 0
        self.died = 0
        self.plan = [['.'] * self.field_w for i in range(self.field_h)]
        self.snake = pygame.sprite.Group()
        self.snake_tail = pygame.sprite.Group()
        self.snake_head = pygame.sprite.Group()
        self.tileset = (load_image('master-tileset.png'), 10, 5)
        self.apple = pygame.transform.scale(cut_sheet((load_image('snake-graphics.png'), 5, 4), (0, 3)),
                                            (self.cell_w, self.cell_h))
        self.now_appls = 0
        self.time = 0
        self.distance = 0
        self.dir_x = 0
        self.dir_y = 0
        self.snake_len = 0
        self.head = None
        self.tail = None

    def new_snake(self, chords, direction):
        self.time = 0
        self.distance = 0
        self.dir_x = direction[0]
        self.dir_y = direction[1]
        self.snake_len = len(chords)
        act = []
        for i in range(0, len(chords)):
            if self.plan[chords[i][1]][chords[i][0]] == '%':
                return False
            x = self.x + chords[i][0] * self.cell_w
            y = self.y + chords[i][1] * self.cell_h
            if i > 0:
                act.append((chords[i - 1][0] - chords[i][0], chords[i - 1][1] - chords[i][1]))
                if i == len(chords) - 1:
                    self.tail = Tail(x, y, self.cell_h, self.cell_w, direction, list(reversed(act)), chords[-1][0],
                                     chords[-1][1], self.snake, self.snake_tail)
                else:
                    self.plan[chords[i][1]][chords[i][0]] = '-'
            else:
                self.head = Head(x, y, self.cell_h, self.cell_w, direction, chords[0][0], chords[0][1],
                                 self.snake, self.snake_head)
        self.plan[chords[-1][1]][chords[-1][0]] = '<'
        self.plan[chords[0][1]][chords[0][0]] = '>'
        return True

    def snake_control(self, time, x, y, screen):
        if self.snake_len == 0:
            return False
        time += self.time
        pixels = time / 1000 * self.cell_w * 3
        move = int(pixels)
        ost = pixels - move
        self.time = ost * 1000 / (self.cell_w * 3)
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
                self.eaten += 1
                self.snake_tail.update(sleep=True)
                self.now_appls -= 1
            self.plan[self.head.y][self.head.x] = '>'
            self.plan[self.tail.y][self.tail.x] = '<'
            hx = self.head.x + self.dir_x
            hy = self.head.y + self.dir_y
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
                self.died += 1
                return False
            else:
                self.snake.update(move=self.distance)
        elif move > 0:
            self.snake.update(move=move)
            self.render(screen)
        if randrange((self.now_appls + 1) * 100) < 1:
            self.summon_apple()
            self.now_appls += 1
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
                else:
                    ch = 0
                    if i == 0 and j == 0:
                        ch = 8
                    im = pygame.transform.scale(cut_sheet(self.tileset, (ch, 2)), (self.cell_w, self.cell_h))
                screen.blit(im, (x, y))
                if cur == '@':
                    screen.blit(self.apple, (x, y))
        self.snake_tail.draw(screen)
        self.snake_head.draw(screen)

    def summon_apple(self):
        if any([any(map(lambda z: z == '.', i)) for i in self.plan]):
            x = randrange(self.field_w)
            y = randrange(self.field_h)
            while self.plan[y][x] != '.' or y == x == 0:
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
        pygame.draw.line(self.image, 'black', (0, self.rect.h), (self.rect.w // 2, 0), self.rect.w // 13)
        pygame.draw.line(self.image, 'black', ((self.rect.w + 1) // 2, 0), (self.rect.w, self.rect.h),
                         self.rect.w // 13)

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
        f = self.order[0]
        if len(self.order) == 1:
            s = (x, y)
        else:
            s = self.order[1]
        tran = self.image
        if f[0] == -1:
            if s[1] == -1:
                tran = pygame.transform.rotate(self.image, -90)
            elif s[1] == 1:
                tran = pygame.transform.rotate(self.image, 90)
        elif f[1] == -1:
            if s[0] == 1:
                tran = pygame.transform.rotate(self.image, -90)
            elif s[0] == -1:
                tran = pygame.transform.rotate(self.image, 90)
        elif f[0] == 1:
            if s[1] == 1:
                tran = pygame.transform.rotate(self.image, -90)
            elif s[1] == -1:
                tran = pygame.transform.rotate(self.image, 90)
        elif f[1] == 1:
            if s[0] == -1:
                tran = pygame.transform.rotate(self.image, -90)
            elif s[0] == 1:
                tran = pygame.transform.rotate(self.image, 90)
        self.image = tran
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


def terminate():
    pygame.quit()
    sys.exit()


def snake_game(screen):
    running = True
    board = Board(0, 0, 1280, 800, 80)
    clock = pygame.time.Clock()
    x = y = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pr = pygame.key.get_pressed()
                x = pr[pygame.K_d] - pr[pygame.K_a]
                y = pr[pygame.K_s] - pr[pygame.K_w]
        report = board.snake_control(clock.tick(50), x, y, screen)
        if not report:
            if not board.new_snake([(0, 0), (0, 0), (0, 0)], (0, 1)):
                return snake_game_over(screen, board.eaten, board.died)
            x = y = 0
        pygame.display.flip()


def snake_game_over(screen, apples, dies):
    all_texts = Surface((screen.get_width(), screen.get_height()))
    all_texts.fill('black')
    go = pygame.font.Font(None, 200).render('GAME OVER', True, 'red')
    all_texts.blit(go, ((screen.get_width() - go.get_width()) // 2, 0))
    y = go.get_height() + 50
    font = pygame.font.Font(None, 75)
    score = apples * 10 - dies * 50
    for i in [f'Собрано яблок: {apples}', f'Змеек погибло: {dies}', 'Формула: Яблоки * 10 - Смерти * 50',
              f'Всего очков: {score}']:
        text = font.render(i, True, 'red')
        all_texts.blit(text, (0, y))
        y += text.get_height() + 50
    ex = pygame.font.Font(None, 125).render('PRESS ANY KEY TO EXIT', True, 'red')
    all_texts.blit(ex, ((screen.get_width() - ex.get_width()) // 2, y))
    y = -screen.get_height()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.QUIT]:
                running = False
        clock.tick(150)
        if y < 0:
            y += 1
            screen.blit(all_texts, (0, y))
            pygame.display.flip()
    return score


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Змейка')
    WIDTH, HEIGHT = 1280, 800
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    snake_game(screen)
    pygame.quit()
