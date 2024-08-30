import os
import pygame as pg
from sys import exit


pg.init()

"""
Персонажем будет котик, который будет ловить колбаски.
За каждую будут начисляться очки.

TODO:
- Исправить коллизии (размеры rect)
- Переписать анимацию персонажа на класс
- Добавить рандом по вылету предметов
- Добавить счёт очков
"""

# Screen
width, height = 1080, 720
screen = pg.display.set_mode((width, height))

fps = 60
clock = pg.time.Clock()

# Даём название окну игры
pg.display.set_caption("Space Cat Game")

# Создаём объект шрифта
text_font = pg.font.Font('prstartk.ttf', 15)

# Создаём поверхность с картинкой
back = pg.image.load(os.path.join("images","landscape.jpg")).convert()
back = pg.transform.scale(back,(1080, 720))

# Создаём заголовок
title_text = text_font.render("Space Cat Game", True, 'White')

# Добавляем игровые объекты (персонаж и предметы)
hero = pg.image.load(os.path.join("Images","cat.png")).convert_alpha()
sausage = pg.image.load(os.path.join("Images","sausage.png")).convert_alpha()
rock = pg.image.load(os.path.join("Images","rock.png")).convert_alpha()
meteor = pg.image.load(os.path.join("Images","meteor.png")).convert_alpha()

# Объявляем начальные координаты для объектов
hero_x_pos = 15
hero_y_pos = 300

sausage_x_pos = 1200
sausage_y_pos = 330

rock_x_pos = 1200
rock_y_pos = 200

meteor_x_pos = 1200
meteor_y_pos = 420

# Помещаем изображение в рамку прямоугольника
# В скобках задаём точку привязки на рамке и координаты для неё
hero_rect = hero.get_rect(center=(hero_x_pos, hero_y_pos))
sausage_rect = sausage.get_rect(center=(sausage_x_pos, sausage_y_pos))
rock_rect = rock.get_rect(center=(rock_x_pos, rock_y_pos))
meteor_rect = meteor.get_rect(center=(meteor_x_pos, meteor_y_pos))

# Создаём сигнальные переменные
star_flag = False
sausage_flag = False
meteor_flag = False

# Текст при столкновении
text_font_collide = pg.font.Font('prstartk.ttf', 35)
text_collide = text_font_collide.render("Game over!", False, 'Red')

# Главный игровой цикл
game = True

while game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        keys = pg.key.get_pressed()

        # Перемещение игрового персонажа
        if keys[pg.K_UP]:
            hero_rect.top -= 20
        if keys[pg.K_DOWN]:
            hero_rect.top += 20
        if keys[pg.K_LEFT]:
            hero_rect.left -= 20
        if keys[pg.K_RIGHT]:
            hero_rect.left += 20
        
        # Возвращаем его к реальности, если персонаж улетел за границу игрового экрана
        if hero_rect.left <= 0:
            hero_rect.left = 0
        if hero_rect.right >= 1080:
            hero_rect.right = 1080
        if hero_rect.top <= 0:
            hero_rect.top = 0
        if hero_rect.bottom >= 720:
            hero_rect.bottom = 720

    # Размещаем все поверхности на экране
    screen.blit(back, (0,0))
    screen.blit(hero, hero_rect)
    screen.blit(rock, rock_rect)
    screen.blit(sausage, sausage_rect)  
    screen.blit(meteor, meteor_rect)
    screen.blit(title_text, (420, 40))

    # Запускаем движение пердметов
    rock_rect.left -= 4
    if rock_rect.left <= 540:
        sausage_flag = True # когда звезда пролетает половину экрана, запускается следующий предмет
    if sausage_flag:
        sausage_rect.left -= 4
    if sausage_rect.left <= 540:
        meteor_flag = True
    if meteor_flag:
        meteor_rect.left -= 4

    # Обнуляем координаты, когда правая грань скрылась за границей игрового экрана
    if rock_rect.right <= 0:
        rock_rect.left = 1080
    if sausage_rect.right <= 0:
        sausage_rect.left = 1080
    if meteor_rect.right <= 0:
        meteor_rect.left = 1280

    # Выводим сообщение о столкновении
    if hero_rect.colliderect(rock_rect) or hero_rect.colliderect(meteor_rect):
        screen.blit(text_collide, (400, 300))

    pg.display.update()
    clock.tick(fps)
