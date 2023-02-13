import pygame
import numpy as np
from pygame.locals import *
import sys
import random
from datetime import datetime

random.seed(datetime.now().timestamp() % 100)
FPS = 2

width, height = 1280, 800
quant = 50

X_cells = 10
Y_cells = int(height / quant) + 1

COLUMNS = 10
ROWS = 16

thick_bound = 5
y_padding = 0
grid_thick = 3
fig_blocks = 4
clock = pygame.time.Clock()
bk_color = (0, 0, 0)

field_color = (64, 64, 64)

amount_figs = 0

figcolors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 128, 0)]
RUNNING = 1
PAUSE = 2
GAMEOVER = 3

state = RUNNING

test = False

start = [7, 15]

row = ['o' for i in range(COLUMNS)]
arr = [row for j in range(ROWS)]
state_field = np.array(arr)
# state_field[0] = np.array( ['a' for i in range(COLUMNS)] )

row = [field_color for i in range(COLUMNS)]
arr = [row for j in range(ROWS)]
color_field = np.array(arr)

r = pygame.Rect((width) / 2 - (X_cells * quant) / 2,
                y_padding,
                X_cells * quant,
                height - y_padding)

score = 0
name = 'Sebastian'
level = 1

I1 = [['o', 'o', 'a', 'o'],
      ['o', 'o', 'a', 'o'],
      ['o', 'o', 'a', 'o'],
      ['o', 'o', 'a', 'o']]

I2 = [['o', 'o', 'o', 'o'],
      ['o', 'o', 'o', 'o'],
      ['o', 'o', 'o', 'o'],
      ['a', 'a', 'a', 'a']]

S11 = [['o', 'o', 'o', 'o'],
       ['o', 'o', 'a', 'o'],
       ['o', 'a', 'a', 'o'],
       ['o', 'a', 'o', 'o']]

S12 = [['o', 'o', 'o', 'o'],
       ['o', 'o', 'o', 'o'],
       ['o', 'a', 'a', 'o'],
       ['o', 'o', 'a', 'a']]

S21 = [['o', 'o', 'o', 'o'],
       ['o', 'a', 'o', 'o'],
       ['o', 'a', 'a', 'o'],
       ['o', 'o', 'a', 'o']]

S22 = [['o', 'o', 'o', 'o'],
       ['o', 'o', 'o', 'o'],
       ['o', 'o', 'a', 'a'],
       ['o', 'a', 'a', 'o']]

T1 = [['o', 'o', 'o', 'o'],
      ['o', 'o', 'o', 'o'],
      ['o', 'a', 'o', 'o'],
      ['a', 'a', 'a', 'o']]

T2 = [['o', 'o', 'o', 'o'],
      ['o', 'o', 'a', 'o'],
      ['o', 'o', 'a', 'a'],
      ['o', 'o', 'a', 'o']]

T3 = [['o', 'o', 'o', 'o'],
      ['o', 'a', 'o', 'o'],
      ['a', 'a', 'o', 'o'],
      ['o', 'a', 'o', 'o']]

T4 = [['o', 'o', 'o', 'o'],
      ['o', 'o', 'o', 'o'],
      ['a', 'a', 'a', 'o'],
      ['o', 'a', 'o', 'o']]

O = [['o', 'o', 'o', 'o'],
     ['o', 'a', 'a', 'o'],
     ['o', 'a', 'a', 'o'],
     ['o', 'o', 'o', 'o']]

L11 = [['o', 'o', 'o', 'o'],
       ['o', 'a', 'o', 'o'],
       ['o', 'a', 'o', 'o'],
       ['o', 'a', 'a', 'o']]

L12 = [['o', 'o', 'o', 'o'],
       ['o', 'o', 'o', 'o'],
       ['o', 'a', 'a', 'a'],
       ['o', 'a', 'o', 'o']]

L13 = [['o', 'o', 'o', 'o'],
       ['o', 'a', 'a', 'o'],
       ['o', 'o', 'a', 'o'],
       ['o', 'o', 'a', 'o']]

L14 = [['o', 'o', 'o', 'o'],
       ['o', 'o', 'o', 'o'],
       ['o', 'o', 'a', 'o'],
       ['a', 'a', 'a', 'o']]

L21 = [['o', 'o', 'o', 'o'],
       ['o', 'o', 'a', 'o'],
       ['o', 'o', 'a', 'o'],
       ['o', 'a', 'a', 'o']]

L22 = [['o', 'o', 'o', 'o'],
       ['o', 'o', 'o', 'o'],
       ['o', 'a', 'o', 'o'],
       ['o', 'a', 'a', 'a']]

L23 = [['o', 'o', 'o', 'o'],
       ['o', 'a', 'a', 'o'],
       ['o', 'a', 'o', 'o'],
       ['o', 'a', 'o', 'o']]

L24 = [['o', 'o', 'o', 'o'],
       ['o', 'o', 'o', 'o'],
       ['a', 'a', 'a', 'o'],
       ['o', 'o', 'a', 'o']]

figures = {"I": [I1, I2],
           "S1": [S11, S12],
           "S2": [S21, S22],
           "T": [T1, T2, T3, T4],
           "O": [O],
           "L1": [L11, L12, L13, L14],
           "L2": [L21, L22, L23, L24]}

# tests for ShowFig
# False - normal work, True - for debugging
test_fig1 = False
test_fig2 = ("S1", 1, figcolors[0])


def draw_fig(fig_key, orientation, color, place, is_area_test=test):
    """
    рисует на отдельном слое по квадратикам фигуру в памяти!
    не на экране
    возвращает ссылку на область памяти где нарисовал (слой)
    и координаты куда вставлять на экране
    is_arae_test - рисовать ли по умолчанию тестовый ореол
    около фигуры, по умолчанию - нет
    """

    # координаты нижней левой точки
    x0 = int((width) / 2 - (X_cells * quant) / 2)
    y0 = int(height)

    # извлекаем место, где рисовать
    x = place[0]
    y = place[1]

    # создание отдельной поверхности для фигуры с возможностью прозрачности
    figure = pygame.Surface((fig_blocks * quant, fig_blocks * quant), pygame.SRCALPHA)

    test_empty_space_color = (255, 0, 0, 64)  # for tests, рисует прилежащую область

    # тут не важны первые три числа, важно что четвертое - ноль, то есть
    # прозрачное - тогда рисовать часть фигуры будет всегда цветом фона
    empty_color = (0, 0, 0, 0)

    r, g, b = color
    color_with_alpha = (r, g, b, 255)

    if is_area_test:
        col = test_empty_space_color
    else:
        col = empty_color

    arr = figures[fig_key][orientation]

    # прорисовка фигуры(спрайта)
    for i in range(fig_blocks):
        for j in range(fig_blocks):
            xa = j * quant
            xb = (j + 1) * quant
            ya = i * quant
            yb = (i + 1) * quant

            rect = pygame.Rect((xa, ya), (xb, yb))

            if arr[i][j] == "a":  # сплошной цвет фигуры рисуем с альфа-каналом
                # рисуем непрозрачный прямоугольник
                # pygame.draw.rect(figure, color, rect)
                figure.fill(color_with_alpha, rect)
            else:  # прозрачный цвет фигуры рисуем, используя альфа-канал
                # pygame.draw.rect(figure, bk_color, rect)
                figure.fill(col, rect)

    # куда вставлять на screen слой клеток 4 на 4
    xs = x - fig_blocks
    ys = y + fig_blocks
    x1 = x0 + xs * quant
    y1 = y0 + quant - ys * quant

    return figure, x1, y1


def set_background(red, green, blue):
    x0 = (width) / 2 - (X_cells * quant) / 2
    pygame.draw.rect(screen, pygame.Color((red, green, blue)), pygame.Rect(x0, y_padding,
                                                                           X_cells * quant,
                                                                           Y_cells * quant - y_padding))

    screen.fill((red, green, blue), rect=(x0, y_padding, X_cells * quant, Y_cells * quant - y_padding))


def DrawFilledCells(screen):
    field = pygame.Surface((X_cells * quant, Y_cells * quant), pygame.SRCALPHA)

    empty_color = (0, 0, 0, 0)

    for i in range(Y_cells - 1):
        for j in range(X_cells):
            k = Y_cells - 1 - 1 - i
            xa = j * quant
            xb = (j + 1) * quant
            ya = k * quant
            yb = (k + 1) * quant

            rect = pygame.Rect((xa, ya), (quant, quant))

            if state_field[i][j] == 'a':
                r, g, b = color_field[i][j]
                color_with_alpha = (r, g, b, 255)

                field.fill(color_with_alpha, rect)
            else:
                field.fill(empty_color, rect)

    x1 = (width) / 2 - (X_cells * quant) / 2
    y1 = y_padding

    screen.blit(field, (x1, y1))


def draw_mainfield(screen, quant):
    screen.fill(field_color, r)
    DrawFilledCells(screen)  # отображение упавших фигур


def DrawGrid(screen):
    x0 = (width) / 2 - (X_cells * quant) / 2
    y0 = (height) / 2 - (Y_cells * quant) / 2

    color_line = (116, 116, 116, 255)

    # рисуем вертикальные линии
    for shift in range(quant, (X_cells - 1) * quant + 1, quant):
        vertical_line = pygame.Surface((grid_thick, height - 2 * thick_bound), pygame.SRCALPHA)
        vertical_line.fill(color_line)  # You can change the 100 depending on what transparency it is.
        screen.blit(vertical_line, (x0 + shift, thick_bound))

    # рисуем горизонтальные линии
    # не соотвествие количеству ячеек прямоугольника по оси y
    for shift in range(quant, (Y_cells - 1) * quant, quant):
        horizontal_line = pygame.Surface((X_cells * quant - 2 * thick_bound, grid_thick), pygame.SRCALPHA)
        horizontal_line.fill(color_line)  # You can change the 100 depending on what transparency it is.
        screen.blit(horizontal_line, (x0 + thick_bound, shift))


def draw_info(screen):
    pygame.font.init()  ###???
    font = pygame.font.SysFont('arial', 45)
    text1 = font.render('Your Name: ', False, pygame.Color('white'))
    text2 = font.render('Level: ', False, pygame.Color('white'))
    text3 = font.render('Score: ', False, pygame.Color('white'))
    text4 = font.render('Time: ', False, pygame.Color('white'))
    text5 = font.render('Next Figure: ', False, pygame.Color('white'))
    text6 = font.render('Amount of Figures: ', False, pygame.Color('white'))

    text_amount = font.render(str(amount_figs), False, pygame.Color('green'))
    text_score = font.render(str(score), False, pygame.Color('green'))
    text_level = font.render(str(level), False, pygame.Color('green'))
    text_name = font.render(str(name), False, pygame.Color('green'))

    # screen.blit(text4, (5, 0))

    screen.blit(text1, (5, 120))
    screen.blit(text_name, (5, 170))

    screen.blit(text2, (5, 240))
    screen.blit(text_level, (5, 290))

    screen.blit(text3, (5, 360))
    screen.blit(text_score, (5, 410))

    screen.blit(text5, (950, 0))

    screen.blit(text6, (950, 400))
    screen.blit(text_amount, (950, 450))


def check_rotation(place, figure, orient):
    x = place[0]
    y = place[1]
    if figure != "O":
        if y > 1:
            return True
        else:
            return False
    else:
        if y > 0:
            return True
        else:
            return False


def OnKeyDown(place, figure, orient, figcol, screen):
    """
    обработчик нажатия кнопки аниз
    """

    button = 2

    x = place[0]
    y = place[1]

    sprite = figures[figure][orient]

    flag = -1  # можно ли перемещаться, -1 - значение неопределено

    # print("down, cango: ", CanGo(button, place, sprite))

    flag = CanGo(button, place, sprite)
    if flag:  # если перемещаться можно, то перемещаемся
        place[1] -= 1

        fig, x1, y1 = draw_fig(figure, orient, figcol, place, test)
        screen.fill((0, 0, 0))
        draw_mainfield(screen, quant)  # make background for field
        screen.blit(fig, (x1, y1))

        DrawGrid(screen)
        draw_info(screen)

        color_grid = (255, 255, 255)
        pygame.draw.rect(screen, color_grid, r, thick_bound)


def OnKeyRight(place, figure, orient, figcol):
    button = 1

    x = place[0]
    y = place[1]

    sprite = figures[figure][orient]
    print("right, cango: ", CanGo(1, place, sprite))

    flag = CanGo(button, place, sprite)

    if flag:  # если перемещаться можно, то перемещаемся
        place[0] += 1


def OnKeyLeft(place, figure, orient, figcol):
    button = 0

    x = place[0]
    y = place[1]

    sprite = figures[figure][orient]

    print("left, cango: ", CanGo(0, place, sprite))

    flag = CanGo(button, place, sprite)

    if flag:  # если перемещаться можно, то перемещаемся
        place[0] -= 1


def OnRotate(place, figure, orient, figcol, screen):
    # если не выходит за пределы то пересчитываем место
    # place может измениться
    if check_rotation(place, figure, orient):
        mx = len(figures[figure])

        # place[0] += 0
        if orient + 1 >= mx:
            orient = 0
        else:
            orient += 1
            fig, x1, y1 = draw_fig(figure, orient, figcol, place, test)
            screen.fill((0, 0, 0))
            draw_mainfield(screen, quant)
            screen.blit(fig, (x1, y1))

            DrawGrid(screen)
            draw_info(screen)

            color_grid = (255, 255, 255)
            pygame.draw.rect(screen, color_grid, r, thick_bound)
    return orient


def CanGo(button, place, sprite):
    """
    вычисляет может ли фигура двигаться в направлении кнопки button
    возвращает True/False
    """
    x = place[0]
    y = place[1]

    flag = -1  # можно ли перемещаться, -1 - значение неопределено

    # проходимся по ячейкам спрайта (фигуры)
    for i in range(fig_blocks):
        for j in range(fig_blocks):
            if sprite[i][j] == 'a':  # если нашли заполненную клетку в фигуре
                # получаем в координатах поля координаты заполненной клетки
                x_test = x - (3 - j)
                y_test = y + (3 - i)

                # проверки:
                if button == 2:  # вниз
                    if y_test - 1 <= 0:  # граница
                        flag = False
                    # y_test - 1 - клетка ниже текущей
                    # еще один минус так как мы переходим к индексу массива вместо
                    # человеческих координат поля с единицы
                    elif y_test - 1 - 1 >= Y_cells - 1:
                        pass
                    elif state_field[y_test - 1 - 1][x_test - 1] == 'a':
                        flag = False
                elif button == 1:  # вправо
                    ###1 и 10 это границы поля, исправить на переменную
                    if x_test + 1 > 10 or x_test + 1 < 1:
                        flag = False
                    elif y_test - 1 >= Y_cells - 1:
                        pass
                    elif state_field[y_test - 1][x_test - 1 + 1] == 'a':
                        flag = False
                elif button == 0:  # влево
                    if x_test - 1 > 10 or x_test - 1 < 1:
                        # print("Перемещаться вправо нельзя!")
                        flag = False
                    elif y_test - 1 >= Y_cells - 1:
                        pass
                    elif state_field[y_test - 1][x_test - 1 - 1] == 'a':
                        flag = False

    # если мы прошлись по фигуре и не поставили False, значит перемещаться можно
    if flag == -1:
        flag = True

    return flag


def ShowNewFig(screen, place, test1=False, test2=("T", 0, 0)):
    if test1:  # нужен тест
        figure = test2[0]
        orient = test2[1]
        figcol = test2[2]
    else:  # обычная работа
        mass = list(figures)
        figure = random.choice(mass)
        orient = random.randint(0, len(figures[figure]) - 1)
        figcol = random.choice(figcolors)

    fig, x1, y1 = draw_fig(figure, orient, figcol, place, test)
    isThereSpace = CheckSpace(figure, orient, place)

    if isThereSpace:
        screen.blit(fig, (x1, y1))
        state = RUNNING
    else:
        state = GAMEOVER

    DrawGrid(screen)

    return figure, orient, figcol, state


def UpdateFieldState(state_field, color_field, place, sprite, figcol):
    """
    обновляет состояние поля: какие клетки заполнены и их цвет
    когда фигура больше перемещаться не может

    результат работы - записывает в первые два массива нужные значения, ничего не возвращает
    """

    x = place[0]
    y = place[1]

    for i in range(fig_blocks):
        for j in range(fig_blocks):
            if sprite[i][j] == 'a':  # если нашли заполненную клетку в фигуре
                # получаем в координатах поля координаты заполненной клетки
                # они начинаются с 1 а не с нуля!
                x_field = x - (3 - j)
                y_field = y + (3 - i)

                state_field[y_field - 1][x_field - 1] = 'a'
                color_field[y_field - 1][x_field - 1] = figcol


def StartScreen(screen):
    x1 = (width) / 2 - (X_cells * quant) / 2
    y1 = height / 2 - 50

    rct = pygame.Rect(x1, y1, quant * X_cells, 200)

    start_screen = pygame.Surface((500, 200), pygame.SRCALPHA)
    start_screen.fill((0, 255, 0, 128))

    font = pygame.font.SysFont('arial', 25)
    text_start = font.render('TETRIS by Sebastian v.0.1 alpha (2023)', False, pygame.Color('magenta'))

    start_screen.blit(text_start, (100, 70))
    screen.blit(start_screen, (x1, y1))


def GaveOverScreen(screen):
    x1 = (width) / 2 - (X_cells * quant) / 2
    y1 = height / 2 - 50

    rct = pygame.Rect(x1, y1, quant * X_cells, 200)

    gameover = pygame.Surface((quant * X_cells, 200), pygame.SRCALPHA)

    gameover.fill((255, 0, 0, 128))

    font = pygame.font.SysFont('arial', 45)
    text_game_over = font.render('GAME OVER!!!', False, pygame.Color('blue'))

    gameover.blit(text_game_over, (100, 70))
    screen.blit(gameover, rct)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.QUIT]:
                running = False


def IsFullRows():
    """
    возвращает кортеж rows_state, rows
    rows_state - True/False есть ли сейчас полные ряды
    rows - списко индексов полных рядов в массиве state_field
    """

    rows_state = False
    rows = []

    for i in range(Y_cells - 1):
        if (np.all(state_field[i] == 'a')):
            rows_state = True
            rows.append(i)

    return rows_state, rows


def RemoveLines(score):
    rows_state, rows = IsFullRows()

    while rows_state == True:
        state_field[rows[0]] = np.array(['o' for i in range(COLUMNS)])
        score += 100 * level

        state_field[rows[0]: len(state_field) - 1][:] = state_field[rows[0] + 1][:]
        state_field[len(state_field) - 1] = np.array(['o' for i in range(COLUMNS)])

        ###############
        ###тут еще надо и массив colors тоже обновлять!!!
        rows_state, rows = IsFullRows()

    return score


def CheckSpace(figure, orient, place):
    sprite = figures[figure][orient]

    x = place[0]
    y = place[1]

    flag = -1  # можно ли перемещаться, -1 - значение неопределено

    # проходимся по ячейкам спрайта (фигуры)
    for i in range(fig_blocks):
        for j in range(fig_blocks):
            if sprite[i][j] == 'a':  # если нашли заполненную клетку в фигуре
                # получаем в координатах поля координаты заполненной клетки
                x_test = x - (3 - j)
                y_test = y + (3 - i)
                k = Y_cells - 1 - 1 - i

                # переводим полевые координаты в индексы массива состояния поля
                if state_field[k][x_test] == 'a':
                    flag = False

        if flag == -1:
            flag = True

    return flag


def tetris_game(screen):
    global score
    global amount_figs
    StartScreen(screen)
    pygame.display.flip()
    pygame.time.wait(500)

    place = start[:]  # положение правого нижнего конца фигуры

    mass = list(figures)
    figure = random.choice(mass)
    orient = random.randint(0, len(figures[figure]) - 1)
    figcol = random.choice(figcolors)

    figure, orient, figcol, state = ShowNewFig(screen, place, test_fig1, test_fig2)
    draw_mainfield(screen, quant)
    DrawGrid(screen)
    draw_info(screen)

    while True:

        keys = pygame.key.get_pressed()

        if state != GAMEOVER:
            if keys[pygame.K_LEFT] or keys[pygame.K_KP4]:
                OnKeyLeft(place, figure, orient, figcol)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_KP6]:
                OnKeyRight(place, figure, orient, figcol)
            elif keys[pygame.K_DOWN] or keys[pygame.K_KP2]:
                OnKeyDown(place, figure, orient, figcol, screen)
            elif keys[pygame.K_SPACE] or keys[pygame.K_KP5]:
                orient = OnRotate(place, figure, orient, figcol, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if state != GAMEOVER:

                if event.type == KEYDOWN:
                    if event.key == K_p:
                        if state == RUNNING:
                            state = PAUSE

                        elif state == PAUSE:
                            state = RUNNING

        if state == RUNNING:
            pygame.time.wait(150)
            OnKeyDown(place, figure, orient, figcol, screen)
            pygame.display.update

            sprite = figures[figure][orient]
            bottom = not (CanGo(2, place, sprite))

            # print("bottom cond: ", bottom, place)

            if bottom:
                # print("bottom cond: ", bottom, place)
                pygame.display.update

                UpdateFieldState(state_field, color_field, place, sprite, figcol)

                amount_figs += 1

                rows_state, rows = IsFullRows()
                print("rows_state: ", rows_state, rows)

                if rows_state:  # если есть целые ряды
                    score = RemoveLines(score)

                place = start[:]
                figure, orient, figcol, state_new = ShowNewFig(screen, place, test_fig1, test_fig2)

                if state_new == GAMEOVER:
                    state = state_new

        if state == GAMEOVER:
            GaveOverScreen(screen)
            return

        pygame.display.flip()


if __name__ == '__main__':
    ###### MAIN CODE
    pygame.init()
    pygame.display.set_caption("Tetris")

    try:
        size = (width, height)

        screen = pygame.display.set_mode(size)

        tetris_game(screen)
    except ValueError:
        print('Неправильный формат ввода')
