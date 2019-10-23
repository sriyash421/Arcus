# "ArcuS"
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>


import pygame
import random
import math
from constants import *
from os import path


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

last_arrow_time = pygame.time.get_ticks()
mouse = pygame.mouse.get_pos()
click = pygame.mouse.get_pressed()

misses = 0
highscore = 0
score = 0
PAUSE = False
with open(HIGHSCORE_FILE, "r") as file:
    highscore = int(file.readline())

arrow_img = pygame.image.load(
    path.join(path.dirname(__file__), ARROW_IMAGE)).convert()
background = pygame.image.load(
    path.join(path.dirname(__file__), BACKGROUND_IMAGE)).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
baloon_color = ["black", "blue", "red", "green"]
explosion = []
for i in range(9):
    filename = "assets/regularExplosion0{}.png".format(i)
    temp = pygame.image.load(
        path.join(path.dirname(__file__), filename)).convert()
    explosion.append(temp)

explosion_sound = pygame.mixer.Sound(
    path.join(path.dirname(__file__), EXPLOSION_SOUND))
select_sound = pygame.mixer.Sound(
    path.join(path.dirname(__file__), CLICK_SOUND))


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, size):
        pygame.sprite.Sprite.__init__(self)
        self.pos = position
        self.size = size
        self.image = pygame.transform.scale(explosion[0], (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.current = pygame.time.get_ticks()
        self.frame_rate = FPS
        self.i = 0
        explosion_sound.play()
        # print(self.i)

    def update(self):
        if(pygame.time.get_ticks()-self.current > self.frame_rate):
            self.i += 1
            # print(self.i)
            if self.i >= len(explosion):
                self.kill()
                return
            self.current = pygame.time.get_ticks()
            self.image = pygame.transform.scale(
                explosion[self.i], (self.size, self.size))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
        self.image.set_colorkey(BLACK)


class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(arrow_img, ARROW_SIZE)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-100
        self.rot = 0
        self.speedx = 0
        self.speedy = 0
        self.range = 0
        self.max_height = 0
        self.release_angle = 0
        self.set_vel = False
        self.Released = False
        self.releasex = self.rect.centerx
        self.releasey = self.rect.bottom
        self.cy = self.rect.centery

    def update(self):
        global last_arrow_time
        if self.Released:
            self.speedy -= GRAVITY
            self.rect.bottom -= self.speedy
            self.rect.centerx += self.speedx
            self.rot = (-math.atan2(self.speedx, self.speedy)*180/3.14) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)

            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            # print "moving"

        else:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if mouse[1] > self.rect.centery and click[0] == 1:
                self.set_vel = True
                dist = math.sqrt(
                    math.pow(self.rect.centerx-mouse[0], 2)+math.pow(self.rect.bottom-mouse[1], 2))
                # print dist

                self.rect.centerx = mouse[0]
                self.rect.centery = mouse[1]
                # print(2*GRAVITY*(self.rect.centery-mouse[1]))
                self.speedy = math.sqrt(2*GRAVITY*(-self.cy+mouse[1]))*4
                self.speedx = self.speedy * \
                    (mouse[0]-self.releasex)/(self.cy-mouse[1])
                self.rot = (-math.atan2(self.speedx, self.speedy)
                            * 180/3.14) % 360
                new_image = pygame.transform.rotate(self.image_orig, self.rot)
                old_center = self.rect.center
                self.image = new_image
                self.rect = self.image.get_rect()
                self.rect.center = old_center

                # print "setting velocity"

            else:
                if self.set_vel:
                    self.Released = True
                    last_arrow_time = pygame.time.get_ticks()
                    self.max_height = (self.rect.bottom-mouse[1])
                    self.range = (mouse[0]-self.rect.centerx)*2
                    # print "releasing"
                # math.sqrt(math.pow(mouse[0]-self.rect.centerx,2)+math.pow(mouse[1]-self.rect.centery,2)) < 200:
                else:
                    if (mouse[0]-self.rect.centerx) != 0:
                        theta = math.atan(
                            (mouse[1]-self.rect.bottom)/(self.rect.centerx-mouse[0]))
                    else:
                        theta = PI
                    move = theta-self.rot
                    self.rot = math.degrees(theta)
                    new_image = pygame.transform.rotate(
                        self.image_orig, self.rot)
                    old_center = self.rect.center
                    self.image = new_image
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
                    # print "rotating"
                    # print self.rot
                    # print theta


class Baloon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        bcolor = random.choice(baloon_color)
        temp = "assets/balloon_{}.png".format(bcolor)
        self.image_orig = pygame.image.load(
            path.join(path.dirname(__file__), temp))
        if bcolor == "blue":
            self.image_orig.set_colorkey(BLUE)
        elif bcolor == "black":
            self.image_orig.set_colorkey(BLACK)
        elif bcolor == "green":
            self.image_orig.set_colorkey(BRIGHT_GREEN)
        elif bcolor == "red":
            self.image_orig.set_colorkey(BRIGHT_RED)

        self.image_orig = pygame.transform.scale(self.image_orig, BALOON_SIZE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = HIT_RADIUS

        temp = random.randrange(WIDTH - self.rect.width)
        while (-150 < temp-WIDTH/2 < 150):
            temp = random.randrange(WIDTH - self.rect.width)
        self.rect.x = temp
        self.rect.y = random.randrange(HEIGHT+100, HEIGHT+150)
        self.speedy = random.randrange(-4, -1)
        self.speedx = random.randrange(-3, 3)
        self.last_update = pygame.time.get_ticks()
        # print "baloon"

    def update(self):
        global misses
        self.rect.y += self.speedy
        if self.rect.top < -20 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.kill()
            misses += 1


def DrawRect(x, y, w, h, c):
    pygame.draw.rect(screen, c, [x, y, w, h])


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def draw_text(text, x, y, s, color):
    font_name = pygame.font.match_font('comicsansms.ttf')
    s = int(s)
    largeText = pygame.font.Font(font_name, s)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = ((x, y))
    screen.blit(TextSurf, TextRect)


def Button(x,y , string, color2, color1, function, w, h):
    global mouse
    global click
    y = int(y) 
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    DrawRect(x, y, w, h, color1)
    if x <= mouse[0] <= x+w and y <= mouse[1] <= y+h:
        DrawRect(x, y, w, int(h), color2)
        if (click[0] == 1):
            select_sound.play()
            function()
    draw_text(string, x+w/2, y+h/2, (w+h)/8, BLACK)


def unpause_function():
    global PAUSE
    PAUSE = False


def pause_function():
    global PAUSE
    PAUSE = True
    while PAUSE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        Button(200, 2*HEIGHT/3, "CONTINUE", BRIGHT_GREEN,
               GREEN, unpause_function, 150, 100)
        Button(WIDTH-450, 2*HEIGHT/3, "QUIT", BRIGHT_RED, RED, quit, 150, 100)
        draw_text("PAUSE", WIDTH/2, HEIGHT/3, 200, BLUE)
        pygame.display.flip()
        clock.tick(FPS)


def replay():
    global score
    global highscore

    if score == highscore:
        with open("assets/highscore.txt", "w") as file:
            file.write("%d" % (score))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(SKY_BLUE)
        screen.blit(background, background_rect)
        Button(200, 2*HEIGHT/3, "PLAY AGAIN",
               BRIGHT_GREEN, GREEN, gameloop, 150, 100)
        Button(WIDTH-450, 2*HEIGHT/3, "QUIT", BRIGHT_RED, RED, quit, 150, 100)
        draw_text("Your Score : %d" % (score), WIDTH/2, HEIGHT/3, 100, BLUE)
        draw_text("HIGH SCORE:%d" % (highscore), WIDTH-400, 50, 30, BLACK)
        if score == highscore:
            draw_text("Congratulations you have a new high score",
                      WIDTH/2, HEIGHT-200, 60, BRIGHT_GREEN)
        pygame.display.flip()
        clock.tick(FPS)


def gameloop():
    global misses
    global highscore
    global score
    global last_arrow_time
    misses = 0
    score = 0
    highscore = 0
    with open("assets/highscore.txt", "r") as file:
        highscore = int(file.readline())
    all_sprites = pygame.sprite.Group()
    arrows = pygame.sprite.Group()
    baloons = pygame.sprite.Group()

    new_arrow = Arrow()
    all_sprites.add(new_arrow)
    arrows.add(new_arrow)
    last_arrow = new_arrow

    new_baloon = Baloon()
    all_sprites.add(new_baloon)
    baloons.add(new_baloon)

    # last_arrow_time = pygame.time.get_ticks()
    last_baloon_time = pygame.time.get_ticks()

    while True:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = pygame.time.get_ticks()
        if last_arrow.Released and now-last_arrow_time > 1000:
            new_arrow = Arrow()
            all_sprites.add(new_arrow)
            arrows.add(new_arrow)
            last_arrow = new_arrow
            # last_arrow_time=now

        if now - last_baloon_time > 2000:
            new_baloon = Baloon()
            all_sprites.add(new_baloon)
            baloons.add(new_baloon)
            last_baloon_time = now

        for baloon in baloons:
            hits = pygame.sprite.spritecollide(
                baloon, arrows, False, pygame.sprite.collide_circle)
            if hits:
                baloon.kill()
                explo = Explosion(baloon.rect.center, 100)
                all_sprites.add(explo)
                score += 1

            if (score > highscore):
                highscore = score

        all_sprites.update()

        if misses > MISSES:
            replay()
        screen.fill(SKY_BLUE)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        Button(WIDTH-120, 20, "PAUSE", BRIGHT_GREEN,
               GREEN, pause_function, 100, 100)
        Button(WIDTH-120, 140, "QUIT", BRIGHT_RED, RED, quit, 100, 100)
        Button(WIDTH-120, 280, "RESTART", BLUE, SKY_BLUE, gameloop, 100, 100)

        draw_text("MISSES : %d" % (misses), WIDTH -
                  200, HEIGHT-150, 50, BRIGHT_RED)
        draw_text("SCORE : %d" % (score), WIDTH-200, HEIGHT-100, 40, BLUE)
        draw_text("HIGH SCORE : %d" % (highscore),
                  WIDTH-200, HEIGHT-50, 40, BLUE)
        pygame.display.flip()


pygame.mixer.music.load(
    (path.join(path.dirname(__file__), "assets/tgfcoder-FrozenJam-SeamlessLoop.ogg")))
pygame.mixer.music.set_volume(VOLUME)

intro = True
while intro:
    pygame.mixer.music.play(loops=-1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro = False

    screen.fill(SKY_BLUE)
    screen.blit(background, background_rect)
    Button(200, 2*HEIGHT/3, "PLAY", BRIGHT_GREEN, GREEN, gameloop, 150, 100)
    Button(WIDTH-450, 2*HEIGHT/3, "QUIT", BRIGHT_RED, RED, quit, 150, 100)
    draw_text("__ArcuS__", WIDTH/2, HEIGHT/3, 200, BLUE)
    draw_text("HIGH SCORE:%d" % (highscore), WIDTH-400, 50, 30, BLACK)
    pygame.display.flip()
    clock.tick(FPS)
