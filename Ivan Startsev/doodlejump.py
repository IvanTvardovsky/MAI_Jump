from random import randint
from sys import exit

import pygame
from pygame.locals import *

pygame.mixer.init()
pygame.init()
pygame.display.set_caption('MAI Jump')


def generate_platform():
    global last_platform
    percent = randint(0, 100)
    if percent < 25 and score > 500:
        last_platform = Monsters(randint(0, 500), last_platform.rect.y - 50)
    if percent < 85:
        last_platform = StandardPlatform(randint(0, 500), last_platform.rect.y - 50)
    elif percent == 99 and score > 100:
        last_platform = BlackHoles(randint(0, 500), last_platform.rect.y - 50)


score = 0


def game_over():
    screen = pygame.display.set_mode((500, 500))
    fon = pygame.image.load("data/game_over.png")
    screen.blit(fon, (0, 0))
    game_font = pygame.font.Font(None, 65)
    string_rendered = game_font.render('Restart', True, pygame.Color('blue'))
    pygame.mouse.set_visible(True)
    rect = string_rendered.get_rect()
    rect.x = 175
    rect.y = 380
    pygame.mixer.music.load("data/gameover.mp3")
    pygame.mixer.music.set_volume(0.4)
    # pygame.mixer.music.play(1)
    screen.blit(string_rendered, rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 380 < event.pos[1] < rect.h + 380 and 175 < event.pos[0] < rect.w + 175:
                    game()
                    exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_answer()
                    pygame.quit()
                    exit(0)


class Doodle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, player)
        self.score = score
        self.image = pygame.image.load("data/doodle.png")
        self.rect = self.image.get_rect()
        self.last_image = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 262
        self.rect.y = 390
        self.time = 0
        self.v = 24
        self.direction = 1
        self.gravity = 1

    def update(self):
        global score, prev
        self.v -= self.gravity
        self.rect.y -= self.v
        if self.v < 0:
            for platform in platform_sprites:
                if pygame.sprite.collide_mask(self, platform):
                    if 40 < platform.rect.y - self.rect.y:
                        self.v = 24
                        pygame.mixer.music.load("data/jump.mp3")
                        pygame.mixer.music.set_volume(0.2)
                        # pygame.mixer.music.play(1)
                        if prev.rect.y > platform.rect.y:
                            score += randint(75, 130)
                            prev = platform
        for hole in holes_sprites:
            if pygame.sprite.collide_mask(self, hole):
                if 3 < hole.rect.y - self.rect.y:
                    game_over()

        for monster in monster_sprite:
            if pygame.sprite.collide_mask(self, monster):
                if -20 < monster.rect.y - self.rect.y:
                    if self.v >= 0:
                        game_over()
                    else:
                        pygame.mixer.music.load("data/jump.mp3")
                        pygame.mixer.music.set_volume(0.2)
                        # pygame.mixer.music.play(1)
                        self.v = 24
                        score += randint(200, 300)
                        monster.kill()
        key = pygame.key.get_pressed()
        if key[K_LEFT]:
            self.image = pygame.image.load("data/doodle.png")
            doodle.rect.x -= 10
        elif key[K_RIGHT]:
            doodle.rect.x += 10
            self.image = pygame.image.load("data/doodle1.png")
        if doodle.rect.x > 620:
            doodle.rect.x = -20
        if doodle.rect.x < -21:
            doodle.rect.x = 619
        if self.rect.y >= 420:
            game_over()

    def update_pos(self, pos):
        self.rect.x += pos


class Monsters(pygame.sprite.Sprite):
    image = pygame.image.load("data/monster.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, monster_sprite)
        self.image = Monsters.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.v = 5

    def update(self):
        self.rect.x += self.v
        if not 0 < self.rect.x < 500:
            self.v = -self.v
        if self.rect.y > 1000:
            self.kill()
            generate_platform()


class StandardPlatform(pygame.sprite.Sprite):
    image = pygame.image.load("data/pl_standard.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, platform_sprites)
        self.image = StandardPlatform.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        if self.rect.y > 1000:
            self.kill()
            generate_platform()


class BlackHoles(pygame.sprite.Sprite):
    image = pygame.image.load("data/hole.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, holes_sprites)
        self.image = BlackHoles.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        if self.rect.y > 800:
            self.kill()
            generate_platform()


class Camera:
    def __init__(self):
        self.dy = 0

    def apply(self, obj):
        obj.rect.y += self.dy

    def update(self, target):
        self.dy = 800 // 2 - (target.rect.y + target.rect.h // 2)


player = pygame.sprite.Group()
holes_sprites = pygame.sprite.Group()
platform_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
camera = Camera()
monster_sprite = pygame.sprite.Group()
doodle = Doodle()
last_platform = 900
font = pygame.font.SysFont("Times New Roman", 25)
prev = StandardPlatform(200, 850)


def info():
    screen = pygame.display.set_mode((600, 600))
    fon = pygame.image.load("data/author_background.png")
    screen.blit(fon, (0, 0))
    menu_font = pygame.font.Font(None, 46)
    font_info = pygame.font.Font(None, 30)
    string = menu_font.render('Авторы:', True, pygame.Color('Blue'))
    author1 = font_info.render('1) Старцев Иван', True, pygame.Color('Black'))
    author2 = font_info.render('2) Филимонов Николай', True, pygame.Color('Black'))
    author3 = font_info.render('3) Шашков Дмитрий', True, pygame.Color('Black'))
    rect = author1.get_rect()
    rect2 = author2.get_rect()
    rect3 = author3.get_rect()
    rect_info = string.get_rect()
    rect.x = 25
    rect.y = 120
    rect2.x = 25
    rect2.y = 170
    rect3.x = 25
    rect3.y = 220
    rect_info.x = 25
    rect_info.y = 40
    screen.blit(author1, rect)
    screen.blit(author2, rect2)
    screen.blit(author3, rect3)
    screen.blit(string, rect_info)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


def game():
    global score, prev
    score = 0
    global player, platform_sprites, all_sprites, \
        doodle, last_platform, holes_sprites, monster_sprite
    size = 600, 800
    screen = pygame.display.set_mode(size)
    player = pygame.sprite.Group()
    platform_sprites = pygame.sprite.Group()
    holes_sprites = pygame.sprite.Group()
    monster_sprite = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    pygame.mouse.set_visible(False)
    game_camera = Camera()
    doodle = Doodle()
    last_platform = StandardPlatform(300, 800)
    prev = StandardPlatform(300, 800)
    for i in range(30):
        generate_platform()
    fon = pygame.image.load("data/background.png").convert()
    screen.blit(fon, (0, 0))
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.blit(fon, (0, 0))
        screen.blit(font.render(str(score), False, (0, 0, 0)), (15, 15))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window_answer()
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_answer()
                    pygame.quit()
                    exit(0)
        all_sprites.update()
        game_camera.update(doodle)
        for sprite in all_sprites:
            game_camera.apply(sprite)
        all_sprites.draw(screen)
        player.draw(screen)
        clock.tick(30)
        pygame.display.flip()


def window_answer():
    screen = pygame.display.set_mode((500, 500))
    fon = pygame.image.load("data/main_background.png")
    screen.blit(fon, (0, 0))
    exit_font = pygame.font.Font(None, 44)
    font_exit = pygame.font.Font(None, 65)
    font_yes = pygame.font.Font(None, 64)
    font_no = pygame.font.Font(None, 64)
    font_slash = pygame.font.Font(None, 80)
    string_rendered = exit_font.render('Вернуться в главное меню', True, pygame.Color('Black'))
    string_exit = font_exit.render('Выйти из игры?', True, pygame.Color('Black'))
    string_yes = font_yes.render('Да', True, pygame.Color('Red'))
    string_slash = font_slash.render('/', True, pygame.Color('Black'))
    string_no = font_no.render('Нет', True, pygame.Color('Green'))
    pygame.mouse.set_visible(True)
    rect_no = string_no.get_rect()
    rect = string_rendered.get_rect()
    rect_exit = string_exit.get_rect()
    rect_yes = string_yes.get_rect()
    rect_slash = string_slash.get_rect()
    rect.x = 50
    rect.y = 375
    rect_exit.x = 70
    rect_exit.y = 140
    rect_yes.x = 110
    rect_yes.y = 250
    rect_slash.x = 250
    rect_slash.y = 247
    rect_no.x = 340
    rect_no.y = 250
    screen.blit(string_rendered, rect)
    screen.blit(string_exit, rect_exit)
    screen.blit(string_yes, rect_yes)
    screen.blit(string_slash, rect_slash)
    screen.blit(string_no, rect_no)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 375 < event.pos[1] < rect.h + 375 and 50 < event.pos[0] < rect.w + 300:
                    main()
                    exit(0)
                if 250 < event.pos[1] < rect_yes.h + 250 and 110 < event.pos[0] < rect_yes.w + 100:
                    pygame.display.quit()
                    pygame.quit()
                    exit(0)
                if 250 < event.pos[1] < rect.h + 250 and 340 < event.pos[0] < rect.w + 100:
                    game()
                    pygame.quit()
                    exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game()
                    pygame.quit()
                    exit(0)


def main():
    screen = pygame.display.set_mode((500, 500))
    fon = pygame.image.load("data/main_background.png")
    screen.blit(fon, (0, 0))
    main_font = pygame.font.Font(None, 65)
    font_info = pygame.font.Font(None, 24)
    string_rendered = main_font.render('Начать игру', True, pygame.Color('Black'))
    string_exit = main_font.render('Выход', True, pygame.Color('Black'))
    author1 = font_info.render('Об авторах', True, pygame.Color('Grey'))
    pygame.mouse.set_visible(True)
    rect = string_rendered.get_rect()
    rect_exit = string_exit.get_rect()
    rect_info = author1.get_rect()
    rect.x = 125
    rect.y = 180
    rect_exit.x = 175
    rect_exit.y = 300
    rect_info.x = 350
    rect_info.y = 450
    pygame.mixer.music.load("data/menu.mp3")
    pygame.mixer.music.set_volume(0.2)
    # pygame.mixer.music.play(-1)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 180 < event.pos[1] < rect.h + 180 and 125 < event.pos[0] < rect.w + 175:
                    pygame.mixer_music.stop()
                    game()
                    pygame.mixer_music.play()
                if 300 < event.pos[1] < rect.h + 300 and 175 < event.pos[0] < rect.w + 175:
                    exit(0)
                if 450 < event.pos[1] < rect.h + 450 and 350 < event.pos[0] < rect.w + 350:
                    info()
            screen = pygame.display.set_mode((500, 500))
            screen.blit(fon, (0, 0))
            pygame.mouse.set_visible(True)
            screen.blit(string_rendered, rect)
            screen.blit(string_exit, rect_exit)
            screen.blit(author1, rect_info)
            pygame.display.flip()


main()
