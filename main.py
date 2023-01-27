import pygame
from pygame.locals import *
import sys
import random
from datetime import datetime

random.seed(datetime.now().timestamp() % 100)
FPS = 50

X_cells = 10
Y_cells = 50
quant = 50
thick_bound = 5
y_padding = 0
grid_thick = 3
fig_blocks = 4
clock = pygame.time.Clock()
bk_color = (0, 0, 0)

figcolors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 128, 0)]

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


def draw_fig(fig_key, orientation, color, place):
    x0 = int((width) / 2 - (X_cells * quant) / 2)
    y0 = int(height)
    x = place[0]
    y = place[1]
    # далее подготовка места (х1,y1) для слоя клеток 4на4
    xs = x - fig_blocks
    ys = y + fig_blocks
    x1 = x0 + xs * quant
    y1 = y0 + quant - ys * quant

    figure = pygame.Surface((fig_blocks * quant, fig_blocks * quant), pygame.SRCALPHA)
    # figure.fill((color[0], color[1], color[2], 100))

    arr = figures[fig_key][orientation]
    for i in range(fig_blocks):
        for j in range(fig_blocks):
            xa = j * quant
            xb = (j + 1) * quant
            ya = i * quant
            yb = (i + 1) * quant
            if arr[i][j] == "a":
                pygame.draw.rect(figure, color, pygame.Rect((xa, ya), (xb, yb)))
            else:
                pygame.draw.rect(figure, bk_color, pygame.Rect((xa, ya), (xb, yb)))

    # for i in range(-1, 1):
    #     screen.set_at((x0 - i, y0 - 10), (255, 0, 0))
    # pygame.draw.circle(screen, (255, 0, 0), (x0, y0 - 10), 10)
    return figure, x1, y1


def movment_fig(screen, place):
    r = 50
    x0 = int((width) / 2 - (X_cells * quant) / 2)
    y0 = int(height)
    x = place[0]
    y = place[1]
    xs = x - fig_blocks
    ys = y + fig_blocks
    x1 = x0 + xs * quant
    y1 = y0 + quant - ys * quant
    screen2 = screen
    '''
    screen - пустой экран или экран до вывода фигуры
    screen2 - совмещеный экран на котором применили фигуру

    '''
    figure = pygame.Surface((fig_blocks * quant, fig_blocks * quant), pygame.SRCALPHA)
    set_background(64, 64, 64)
    draw_mainfield(screen, quant)
    '''
    в будущем требуется в данном месте сохранять текущие состояне
     экрана в переменную и затем ее востанвливать 
     '''


def set_background(red, green, blue):
    x0 = (width) / 2 - (X_cells * quant) / 2
    pygame.draw.rect(screen, pygame.Color((red, green, blue)), pygame.Rect(x0, y_padding,
                                                                           X_cells * quant,
                                                                           Y_cells * quant - y_padding))
    screen.fill((red, green, blue), rect=(x0, y_padding, X_cells * quant, Y_cells * quant - y_padding))


def draw_mainfield(screen, quant):
    '''
    Проверить параметры разрешение по Y и quant
    :param screen:
    :param quant:
    :return:
    '''
    pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect((width) / 2 - (X_cells * quant) / 2, y_padding,
                                                                X_cells * quant,
                                                                height - y_padding), thick_bound)
    x0 = (width) / 2 - (X_cells * quant) / 2
    y0 = (height) / 2 - (Y_cells * quant) / 2
    for shift in range(quant, (X_cells - 1) * quant + 1, quant):
        vertical_line = pygame.Surface((grid_thick, height - 2 * thick_bound), pygame.SRCALPHA)
        vertical_line.fill((116, 116, 116, 100))  # You can change the 100 depending on what transparency it is.
        screen.blit(vertical_line, (x0 + shift, thick_bound))

    # не соотвествие количеству ячеек прямоугольника по оси y
    for shift in range(quant, (Y_cells - 1) * quant, quant):
        horizontal_line = pygame.Surface((X_cells * quant - 2 * thick_bound, grid_thick), pygame.SRCALPHA)
        horizontal_line.fill((116, 116, 116, 100))  # You can change the 100 depending on what transparency it is.
        screen.blit(horizontal_line, (x0 + thick_bound, shift))


def draw_info(screen):
    pygame.font.init()
    font = pygame.font.SysFont('arial', 45)
    text1 = font.render('Your Name: ', False, pygame.Color('white'))
    text2 = font.render('Level: ', False, pygame.Color('white'))
    text3 = font.render('Score: ', False, pygame.Color('white'))
    text4 = font.render('Time: ', False, pygame.Color('white'))
    text5 = font.render('Type of Figure: ', False, pygame.Color('white'))

    screen.blit(text4, (5, 0))
    screen.blit(text1, (5, 100))
    screen.blit(text2, (5, 200))
    screen.blit(text3, (5, 300))
    screen.blit(text5, (950, 0))


def check_limits(place, button, fig, orient):
    x = place[0]
    y = place[1]
    if fig == "I":
        if orient == 0:
            if button == 1:
                if x == X_cells - 1 + 2:
                    return False
                else:
                    return True
            if button == 0:
                if x == 2:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
        if orient == 1:
            if button == 1:
                if x == X_cells - 1 + 1:
                    return False
                else:
                    return True
            if button == 0:
                if x == 4:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True

    if fig == "O":
        if orient == 0:
            if button == 1:
                if x == X_cells - 1 + 2:
                    return False
                else:
                    return True
            if button == 0:
                if x == 3:
                    return False
                else:
                    return True
            if button == 2:
                if y == 0:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
        if orient == 1:
            return True
    if fig == "T":
        if orient == 0:
            if button == 1:
                if x == X_cells - 1 + 2:
                    return False
                else:
                    return True
            if button == 0:
                if x == 4:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
        if orient == 1:
            if button == 1:
                if x == X_cells - 1 + 1:
                    return False
                else:
                    return True
            if button == 0:
                if x == 2:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
        if orient == 2:
            if button == 1:
                if x == X_cells - 1 + 3:
                    return False
                else:
                    return True
            if button == 0:
                if x == 4:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
        if orient == 3:
            if button == 1:
                if x == X_cells - 1 + 2:
                    return False
                else:
                    return True
            if button == 0:
                if x == 4:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
    if fig == "S1":
        if orient == 0:
            if button == 1:
                if x == X_cells - 1 + 2:
                    return False
                else:
                    return True
            if button == 0:
                if x == 3:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
        if orient == 1:
            if button == 1:
                if x == X_cells - 1 + 1:
                    return False
                else:
                    return True
            if button == 0:
                if x == 3:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True


    if fig == "S2":
        if orient == 0:
            if button == 1:
                if x == X_cells - 1 + 2:
                    return False
                else:
                    return True
            if button == 0:
                if x == 3:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
        if orient == 1:
            if button == 1:
                if x == X_cells - 1 + 1:
                    return False
                else:
                    return True
            if button == 0:
                if x == 3:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True

    if fig == "L1":
        if orient == 0:
            if button == 1:
                if x == X_cells - 1 + 2:
                    return False
                else:
                    return True
            if button == 0:
                if x == 3:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
        if orient == 1:
            if button == 1:
                if x == X_cells - 1 + 1:
                    return False
                else:
                    return True
            if button == 0:
                if x == 3:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
        if orient == 2:
            if button == 1:
                if x == X_cells - 1 + 2:
                    return False
                else:
                    return True
            if button == 0:
                if x == 3:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
        if orient == 3:
            if button == 1:
                if x == X_cells - 1 + 2:
                    return False
                else:
                    return True
            if button == 0:
                if x == 4:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True

    if fig == "L2":
        if orient == 0:
            if button == 1:
                if x == X_cells - 1 + 2:
                    return False
                else:
                    return True
            if button == 0:
                if x == 3:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
        if orient == 1:
            if button == 1:
                if x == X_cells - 1 + 1:
                    return False
                else:
                    return True
            if button == 0:
                if x == 3:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
        if orient == 2:
            if button == 1:
                if x == X_cells - 1 + 2:
                    return False
                else:
                    return True
            if button == 0:
                if x == 3:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True
        if orient == 3:
            if button == 1:
                if x == X_cells - 1 + 2:
                    return False
                else:
                    return True
            if button == 0:
                if x == 4:
                    return False
                else:
                    return True
            if button == 2:
                if y == 1:
                    return False
                else:
                    return True
            if button == 3:
                if y + 3 == 16:
                    return False
                else:
                    return True

def OnKeyDown(place, figure, orient):
    """
    обработчик нажатия кнопки аниз
    """
    button = 2
    if check_limits(place, button, figure, orient):
        place[1] -= 1
        fig, x1, y1 = draw_fig(figure, orient, figcolors[3], place)
        screen.fill((0, 0, 0))
        field_state.blit(fig, (x1, y1))
        draw_mainfield(screen, quant)
        draw_info(screen)


def OnKeyUp(place, figure, orient):
    """
    обработчик нажатия кнопки вверх
    """
    button = 3
    if check_limits(place, button, figure, orient):
        place[1] += 1
        fig, x1, y1 = draw_fig(figure, orient, figcolors[3], place)
        screen.fill((0, 0, 0))
        field_state.blit(fig, (x1, y1))
        draw_mainfield(screen, quant)
        draw_info(screen)


def OnKeyRight(place, figure, orient):
    button = 1
    if check_limits(place, button, figure, orient):  # and checkPos(cup, fallingFig, adjX=1):
        place[0] += 1
        fig, x1, y1 = draw_fig(figure, orient, figcolors[3], place)
        screen.fill((0, 0, 0))
        field_state.blit(fig, (x1, y1))
        draw_mainfield(screen, quant)
        draw_info(screen)
        # filed_old = field_state
        # screen.fill((0, 0, 0))
        # screen.blit(fig, (x1, y1))
        # draw_mainfield(screen, quant)
        # draw_info(screen)
        # screen = field_state
        # field_state = filed_old


def OnKeyLeft(place, figure, orient):
    button = 0
    if check_limits(place, button, figure, orient):
        place[0] -= 1
        fig, x1, y1 = draw_fig(figure, orient, figcolors[3], place)
        screen.fill((0, 0, 0))
        field_state.blit(fig, (x1, y1))
        draw_mainfield(screen, quant)
        draw_info(screen)

        # filed_old = field_state
        # screen.fill((0, 0, 0))
        # field_state.blit(fig, (x1, y1))
        # draw_mainfield(screen, quant)
        # draw_info(screen)
        # screen = field_state
        # field_state = filed_old


# def main():
# if __name__ == '__main__':
pygame.init()
pygame.display.set_caption("Tetris")

try:
    width, height = 1280, 800
    size = (width, height)

    A = ((width) / 2 - (height * quant) / 2, height)
    B = ((width) / 2 - (height * quant) / 2, 0)
    C = ((width) / 2 + (height * quant) / 2, 0)
    D = ((width) / 2 + (height * quant) / 2, height)

    screen = pygame.display.set_mode(size)
    draw_info(screen)
    draw_mainfield(screen, quant)

    # movment_fig(screen, (5, 5))
    place = [10, 12]  # положение правого нижнего конца фигуры

    figure = "L2"
    orient = 3
    print("Debug: ", figure, orient)
    fig, x1, y1 = draw_fig(figure, orient, figcolors[3], place)
    field_state = screen
    screen.fill((0, 0, 0))
    field_state.blit(fig, (x1, y1))
    draw_mainfield(screen, quant)
    draw_info(screen)

    """
    1. как сделать чтобы когда держишь кнопку фигура перемещалась постоянно не останавливаясь?
    2. делать проверку может ли переместиться фигура
    3. сетка и рисовать поверх

    домашка от 22012023
    А. сделать чтобы во все стороны не рисовало шлейф
    Б. рисовать в фигуре не черные прямоугольники где фигуры нет а прозрачные тогда будет видна и сетка и границы
    В. сделать проверки на выход
    Г. пункт 1 выше

    """

    while True:
        """
        сначала проверка может ли встать туда куда мы нажали фигура
        берем place и создаем временный новый place и проверяем может ли он быть таким
        если да - то place = place_new
        и стираем старую фигуру
        рисуем новую с помощью draw_fig в новом месте
        если нет - игнорим нажатие                    
        """

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_KP4 or event.key == K_LEFT:  # and checkPos(cup, fallingFig, adjX=-1):
                    OnKeyLeft(place, figure, orient)
                elif event.key == K_KP6 or event.key == K_RIGHT:
                    OnKeyRight(place, figure, orient)
                elif event.key == K_KP8 or event.key == K_UP:
                    OnKeyUp(place, figure, orient)
                elif event.key == K_KP2 or event.key == K_DOWN:
                    OnKeyDown(place, figure, orient)

        pygame.time.wait(200)
        # pygame.event.Event(KEYDOWN, K_DOWN)

        OnKeyDown(place, figure, orient)

        pygame.display.flip()

    # # это позволяет сразу не закрывать окно после отрисовки фигуры, а оно живет пока не закроем программу явно
    # while pygame.event.wait().type != pygame.QUIT:
    #     pygame.display.flip()
    # pygame.display.flip()
    # pygame.time.delay(3000)

    # x0 = int((width) / 2 - (X_cells * quant) / 2)
    # y0 = int(height)

except ValueError:
    print('Неправильный формат ввода')

# главный цикл игры

# while True:


# main()
