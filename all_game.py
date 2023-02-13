import pygame
import sys
import os
from pygame import Surface
from snake import snake_game
from tetris import tetris_game


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


def render_record_table(screen):
    screen.fill('white')
    headline = pygame.font.Font(None, 150).render('Последние результаты', True, 'black')
    screen.blit(headline, ((screen.get_width() - headline.get_width()) // 2, 0))
    y = headline.get_height() + 10
    font = pygame.font.Font(None, 100)
    exit_txt = font.render('Нажмите любую кнопку для выхода', True, 'black')
    snake_txt = font.render('Змейка', True, 'black')
    tetris_txt = font.render('Тетрис', True, 'black')
    screen.blit(exit_txt, ((screen.get_width() - exit_txt.get_width()) // 2, y))
    y += 78
    screen.blit(snake_txt, ((screen.get_width() // 2 - snake_txt.get_width()) // 2, y))
    screen.blit(tetris_txt, ((screen.get_width() * 3 // 2 - tetris_txt.get_width()) // 2, y))
    ys = yt = y + 68
    for i in open('data/records.txt', encoding='utf8').read().split('\n')[:-1]:
        ty, sc = i.split(' ')
        if min(ys, yt) + 68 > screen.get_height():
            break
        if ty == 'Змейка' and ys + 78 > screen.get_height() or ty == 'Тетрис' and yt + 68 > screen.get_height():
            continue
        txt = font.render(sc, True, 'black')
        if ty == 'Змейка':
            screen.blit(txt, ((screen.get_width() // 2 - txt.get_width()) // 2, ys))
            ys += 68
        else:
            screen.blit(txt, ((screen.get_width() * 3 // 2 - txt.get_width()) // 2, yt))
            yt += 68
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.QUIT]:
                running = False


def render_main_menu(screen):
    font = pygame.font.Font(None, 100)
    screen.blit(pygame.transform.scale(load_image('snake_logo.png'),
                                       (screen.get_width(), screen.get_height() // 2)), (0, 0))
    screen.blit(pygame.transform.scale(load_image('tetris_logo.jpg'),
                                       (screen.get_width(), screen.get_height() // 2)), (0, screen.get_height() // 2))
    snake_txt = font.render('Играть в Змейку', True, 'black')
    screen.blit(snake_txt, ((screen.get_width() - snake_txt.get_width()) // 2,
                            screen.get_height() // 2 - snake_txt.get_height() - 10))
    tetris_txt = font.render('Играть в Тетрис', True, 'black')
    screen.blit(tetris_txt, ((screen.get_width() - snake_txt.get_width()) // 2,
                             screen.get_height() - snake_txt.get_height() - 10))
    record_table = Surface(((screen.get_width() + 1) // 5, screen.get_height() // 2))
    record_table.fill('white')
    record_table.blit(pygame.font.Font(None, 50).render('Последние', True, 'black'), (0, 0))
    record_table.blit(pygame.font.Font(None, 50).render('результаты', True, 'black'), (0, record_table.get_height() // 2))
    screen.blit(record_table, (0, screen.get_height() // 2))
    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Двойная игра')
    WIDTH, HEIGHT = 1280, 800
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    running = True
    render_main_menu(screen)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                x, y = event.pos
                recs = open('data/records.txt', 'r', encoding='utf-8').read()
                if y <= HEIGHT // 2:
                    recs = f'Змейка {snake_game(screen)}\n' + recs
                    open('data/records.txt', 'w', encoding='utf-8').write(recs)
                else:
                    if x > WIDTH // 5:
                        # Тетрис проклят, не лезьте сюда
                        # P.S После сбора линии я проиграл
                        tetris_game(screen)
                        # Здесь я должен получить счёт, набранный в процессе игры в тетрис
                        # Но я не смог набрать ни одного очка
                        recs = f'Тетрис {0}\n' + recs
                        open('data/records.txt', 'w', encoding='utf-8').write(recs)
                    else:
                        render_record_table(screen)
                render_main_menu(screen)
    pygame.quit()
