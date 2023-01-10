from random import randint
from sys import exit

import pygame
from pygame.locals import *

pygame.mixer.init()
pygame.init()
pygame.display.set_caption('MAI Jump')

score = 0
frequency = randint(5, 10)


def GeneratePlatform():
    global lastPlatform
    percent = randint(0, 100)
    if (score % (frequency * 1000) <
            (frequency * 1000 - 300) % (frequency * 1000) <
            (score + 1000) % (frequency * 1000) + 1000):
        lastPlatform = FragilePlatform(randint(0, 500), lastPlatform.rect.y - 50)
    else:
        if percent < 25 and score > 500:
            lastPlatform = Monster(randint(0, 500), lastPlatform.rect.y - 50)
        if percent < 85:
            lastPlatform = StandardPlatform(randint(0, 500), lastPlatform.rect.y - 50)
        elif percent < 95:
            lastPlatform = MovingPlatform(randint(10, 490), lastPlatform.rect.y - 50)
        elif percent < 99:
            lastPlatform = BrokenPlatform(randint(0, 500), lastPlatform.rect.y - 50)
        elif percent == 99 and score > 100:
            lastPlatform = BlackHole(randint(0, 500), lastPlatform.rect.y - 50)


def GameOver():
    screen = pygame.display.set_mode((500, 500))
    fon = pygame.image.load("data/game_over.png")
    screen.blit(fon, (0, 0))
    gameFont = pygame.font.Font(None, 65)
    stringRender = gameFont.render('Restart', True, pygame.Color('blue'))
    pygame.mouse.set_visible(True)
    rect = stringRender.get_rect()
    rect.x = 175
    rect.y = 380
    pygame.mixer.music.load("data/gameover.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(1)
    screen.blit(stringRender, rect)
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


class Jumper(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(allSprites, player)
        self.score = score
        self.image = pygame.image.load("data/jumper.png")
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
            for platform in platformSprites:
                if pygame.sprite.collide_mask(self, platform):
                    if 40 < platform.rect.y - self.rect.y:
                        self.v = 24
                        pygame.mixer.music.load("data/jump.mp3")
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(1)
                        if prev.rect.y > platform.rect.y:
                            score += randint(75, 130)
                            prev = platform
        if self.v < 0:
            for platform in fragilePlatformSprites:
                if pygame.sprite.collide_mask(self, platform):
                    if 40 < platform.rect.y - self.rect.y:
                        self.v = 24
                        pygame.mixer.music.load("data/jump.mp3")
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(1)
                        if prev.rect.y > platform.rect.y:
                            prev = platform
                            score += randint(75, 130)
                        platform.jump()
        for hole in blackHoleSprites:
            if pygame.sprite.collide_mask(self, hole):
                if 3 < hole.rect.y - self.rect.y:
                    GameOver()

        for monster in monsterSprites:
            if pygame.sprite.collide_mask(self, monster):
                if -20 < monster.rect.y - self.rect.y:
                    if self.v >= 0:
                        GameOver()
                    else:
                        pygame.mixer.music.load("data/jump.mp3")
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(1)
                        self.v = 24
                        score += randint(200, 300)
                        monster.kill()
        key = pygame.key.get_pressed()
        if key[K_LEFT]:
            self.image = pygame.image.load("data/jumper.png")
            jumper.rect.x -= 10
        elif key[K_RIGHT]:
            jumper.rect.x += 10
            self.image = pygame.image.load("data/jumper1.png")
        if jumper.rect.x > 620:
            jumper.rect.x = -20
        if jumper.rect.x < -21:
            jumper.rect.x = 619
        if self.v < 0:
            for platform in brokenPlatformSprites:
                if pygame.sprite.collide_mask(self, platform):
                    if 40 < platform.rect.y - self.rect.y:
                        platform.jump()
        if self.rect.y >= 420:
            GameOver()

    def updatePos(self, pos):
        self.rect.x += pos


class Monster(pygame.sprite.Sprite):
    image = pygame.image.load("data/monster.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(allSprites, monsterSprites)
        self.image = Monster.image
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
            GeneratePlatform()


class StandardPlatform(pygame.sprite.Sprite):
    image = pygame.image.load("data/pl_standard.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(allSprites, platformSprites)
        self.image = StandardPlatform.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        if self.rect.y > 1000:
            self.kill()
            GeneratePlatform()


class FragilePlatform(pygame.sprite.Sprite):
    image = pygame.image.load("data/pl_fragile.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(allSprites, fragilePlatformSprites)
        self.image = FragilePlatform.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        if self.rect.y > 1000:
            self.kill()
            GeneratePlatform()

    def jump(self):
        self.kill()
        deadPlatformSprites.add(self)
        GeneratePlatform()


class MovingPlatform(pygame.sprite.Sprite):
    image = pygame.image.load("data/pl_moving.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(allSprites, platformSprites)
        self.image = MovingPlatform.image
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
            GeneratePlatform()


class BrokenPlatform(pygame.sprite.Sprite):
    image = pygame.image.load("data/pl_broken_stable.png")
    image2 = pygame.image.load("data/pl_broken_unstable.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(allSprites, brokenPlatformSprites)
        self.image = BrokenPlatform.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.gravity = 0
        self.v = 0

    def jump(self):
        self.image = BrokenPlatform.image2
        self.gravity = 1
        self.v = 2
        pos_x, pos_y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y + 1

    def update(self):
        self.rect.y += self.v
        self.v += self.gravity
        if self.rect.y > 1000:
            self.kill()
            GeneratePlatform()


class BlackHole(pygame.sprite.Sprite):
    image = pygame.image.load("data/hole.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(allSprites, blackHoleSprites)
        self.image = BlackHole.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        if self.rect.y > 800:
            self.kill()
            GeneratePlatform()


class Camera:
    def __init__(self):
        self.dy = 0

    def apply(self, obj):
        obj.rect.y += self.dy

    def update(self, target):
        self.dy = 800 // 2 - (target.rect.y + target.rect.h // 2)


player = pygame.sprite.Group()
blackHoleSprites = pygame.sprite.Group()
platformSprites = pygame.sprite.Group()
brokenPlatformSprites = pygame.sprite.Group()
allSprites = pygame.sprite.Group()
fragilePlatformSprites = pygame.sprite.Group()
camera = Camera()
deadPlatformSprites = pygame.sprite.Group()
monsterSprites = pygame.sprite.Group()
jumper = Jumper()
lastPlatform = 900
font = pygame.font.SysFont("Times New Roman", 25)
prev = StandardPlatform(200, 850)


def info():
    screen = pygame.display.set_mode((600, 600))
    fon = pygame.image.load("data/author_background.png")
    screen.blit(fon, (0, 0))
    menuFont = pygame.font.Font(None, 46)
    fontInfo = pygame.font.Font(None, 30)
    string = menuFont.render('Авторы:', True, pygame.Color('Blue'))
    author1 = fontInfo.render('1) Старцев Иван', True, pygame.Color('Black'))
    author2 = fontInfo.render('2) Филимонов Николай', True, pygame.Color('Black'))
    author3 = fontInfo.render('3) Шашков Дмитрий', True, pygame.Color('Black'))
    rect = author1.get_rect()
    rect2 = author2.get_rect()
    rect3 = author3.get_rect()
    rectInfo = string.get_rect()
    rect.x = 25
    rect.y = 120
    rect2.x = 25
    rect2.y = 170
    rect3.x = 25
    rect3.y = 220
    rectInfo.x = 25
    rectInfo.y = 40
    screen.blit(author1, rect)
    screen.blit(author2, rect2)
    screen.blit(author3, rect3)
    screen.blit(string, rectInfo)
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
    global player, platformSprites, brokenPlatformSprites, allSprites, \
        jumper, lastPlatform, blackHoleSprites, monsterSprites
    size = 600, 800
    screen = pygame.display.set_mode(size)
    player = pygame.sprite.Group()
    platformSprites = pygame.sprite.Group()
    blackHoleSprites = pygame.sprite.Group()
    monsterSprites = pygame.sprite.Group()
    brokenPlatformSprites = pygame.sprite.Group()
    allSprites = pygame.sprite.Group()
    pygame.mouse.set_visible(False)
    gameCamera = Camera()
    jumper = Jumper()
    lastPlatform = StandardPlatform(300, 800)
    prev = StandardPlatform(300, 800)
    for i in range(30):
        GeneratePlatform()
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
        allSprites.update()
        gameCamera.update(jumper)
        for sprite in allSprites:
            gameCamera.apply(sprite)
        allSprites.draw(screen)
        player.draw(screen)
        clock.tick(30)
        pygame.display.flip()


def window_answer():
    screen = pygame.display.set_mode((500, 500))
    fon = pygame.image.load("data/main_background.png")
    screen.blit(fon, (0, 0))
    exitFont = pygame.font.Font(None, 44)
    fontExit = pygame.font.Font(None, 65)
    fontYes = pygame.font.Font(None, 64)
    fontNo = pygame.font.Font(None, 64)
    fontSlash = pygame.font.Font(None, 80)
    stringRender = exitFont.render('Вернуться в главное меню', True, pygame.Color('Black'))
    stringExit = fontExit.render('Выйти из игры?', True, pygame.Color('Black'))
    stringYes = fontYes.render('Да', True, pygame.Color('Red'))
    stringSlash = fontSlash.render('/', True, pygame.Color('Black'))
    stringNo = fontNo.render('Нет', True, pygame.Color('Green'))
    pygame.mouse.set_visible(True)
    rectNo = stringNo.get_rect()
    rect = stringRender.get_rect()
    rectExit = stringExit.get_rect()
    rectYes = stringYes.get_rect()
    rectSlash = stringSlash.get_rect()
    rect.x = 50
    rect.y = 375
    rectExit.x = 70
    rectExit.y = 140
    rectYes.x = 110
    rectYes.y = 250
    rectSlash.x = 250
    rectSlash.y = 247
    rectNo.x = 340
    rectNo.y = 250
    screen.blit(stringRender, rect)
    screen.blit(stringExit, rectExit)
    screen.blit(stringYes, rectYes)
    screen.blit(stringSlash, rectSlash)
    screen.blit(stringNo, rectNo)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 375 < event.pos[1] < rect.h + 375 and 50 < event.pos[0] < rect.w + 300:
                    main()
                    exit(0)
                if 250 < event.pos[1] < rectYes.h + 250 and 110 < event.pos[0] < rectYes.w + 100:
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
    mainFont = pygame.font.Font(None, 65)
    fontInfo = pygame.font.Font(None, 24)
    stringRender = mainFont.render('Начать игру', True, pygame.Color('Black'))
    stringExit = mainFont.render('Выход', True, pygame.Color('Black'))
    author1 = fontInfo.render('Об авторах', True, pygame.Color('Grey'))
    pygame.mouse.set_visible(True)
    rect = stringRender.get_rect()
    rectExit = stringExit.get_rect()
    rectInfo = author1.get_rect()
    rect.x = 125
    rect.y = 180
    rectExit.x = 175
    rectExit.y = 300
    rectInfo.x = 350
    rectInfo.y = 450
    pygame.mixer.music.load("data/menu.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
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
            screen.blit(stringRender, rect)
            screen.blit(stringExit, rectExit)
            screen.blit(author1, rectInfo)
            pygame.display.flip()


main()
