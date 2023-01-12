import pygame

X_cells = 10
Y_cells = 50
quant = 50
thick_bound = 5
y_padding = 0
grid_thick = 3
fig_blocks = 4

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
      ['o', 'o', 'a', 'o'],
      ['o', 'a', 'a', 'a']]

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


def draw_fig(screen, fig_key, orientation, color, place):
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

    screen.blit(figure, (x1, y1))
    # for i in range(-1, 1):
    #     screen.set_at((x0 - i, y0 - 10), (255, 0, 0))
    # pygame.draw.circle(screen, (255, 0, 0), (x0, y0 - 10), 10)


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


if __name__ == '__main__':
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
        print(type(screen))
        draw_mainfield(screen, quant)
        draw_info(screen)

        draw_fig(screen, "S2", 0, figcolors[3], (5, 2))
        # x0 = int((width) / 2 - (X_cells * quant) / 2)
        # y0 = int(height)
        while pygame.event.wait().type != pygame.QUIT:
            pygame.display.flip()
            # pygame.quit()
    except ValueError:
        print('Неправильный формат ввода')
