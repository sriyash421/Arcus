import pygame
import random
import math
from constants import *
from os import path
from objects import *
from animation import *

# Game Class has in game functions
class Game :
    def __init__(self) :
        pygame.init()

        #detecting screen size and storing
        displayInfoObject = pygame.display.Info()
        self.WIDTH = displayInfoObject.current_w - 20
        self.HEIGHT = displayInfoObject.current_h - 20

        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        pygame.display.set_caption("Arcus")
        self.clock = pygame.time.Clock()
        self.last_arrow_time = pygame.time.get_ticks()
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        self.draw = Draw(self)
        self.misses = 0
        self.highscore = 0
        self.score = 0
        self.PAUSE = False
        self.highscore = 0
        self.arrow_img = pygame.image.load(
                path.join(path.dirname(__file__), ARROW_IMAGE)).convert()
        self.background = pygame.image.load(
                path.join(path.dirname(__file__), BACKGROUND_IMAGE)).convert()
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.background_rect = self.background.get_rect()
        self.baloon_color = ["black", "blue", "red", "green"]
        self.time_restricted_mode = False

        self.all_sprites = None
        self.baloons = None
        self.arrows = None
        self.new_baloon = None
        self.new_arrow = None
        self.last_arrow = None
        self.last_baloon_time = 0
        self.last_arrow_time = 0

        self.explosion = []
        for i in range(9):
            filename = "assets/regularExplosion0{}.png".format(i)
            temp = pygame.image.load(
                path.join(path.dirname(__file__), filename)).convert()
            self.explosion.append(temp)

        self.explosion_sound = pygame.mixer.Sound(
            path.join(path.dirname(__file__), EXPLOSION_SOUND))
        self.select_sound = pygame.mixer.Sound(
            path.join(path.dirname(__file__), CLICK_SOUND))

    def readHighScore(self) :
        try :
            with open(HIGHSCORE_FILE, "r") as file:
                self.highscore = int(file.readline())
        except :
            self.highscore = 0
    
    def writeHighScore(self) :
        with open(HIGHSCORE_FILE, "w") as file:
                file.write("%d" % (self.score))

    def loadMusic(self):
        pygame.mixer.music.load(
            (path.join(path.dirname(__file__), "assets/tgfcoder-FrozenJam-SeamlessLoop.ogg")))
        pygame.mixer.music.set_volume(VOLUME)

    def unpause_function(self):
        self.PAUSE = False


    def pause_function(self):
        self.PAUSE = True
        while self.PAUSE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            self.screen.fill(SKY_BLUE)
            self.screen.blit(self.background, self.background_rect)
            self.draw.Button(200, 2*self.HEIGHT/3, "CONTINUE", BRIGHT_GREEN,
               GREEN, self.unpause_function, 150, 100)
            self.draw.Button(self.WIDTH-450, 2*self.HEIGHT/3, "QUIT", BRIGHT_RED, RED, quit, 150, 100)
            self.draw.draw_text("PAUSE", self.WIDTH/2, self.HEIGHT/3, 200, BLUE)
            pygame.display.flip()
            self.clock.tick(FPS)

    def time_restricted(self):
        self.time_restricted_mode = True
        self.gameloop()

    def replay(self):
        if self.score == self.highscore:
            self.writeHighScore()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                self.screen.fill(SKY_BLUE)
                self.screen.blit(self.background, self.background_rect)
                self.draw.Button(200, 2*self.HEIGHT/3, "PLAY AGAIN",
                    BRIGHT_GREEN, GREEN, self.gameloop, 150, 100)
                self.draw.Button(self.WIDTH/2 - 75, 2*self.HEIGHT/3, "PLAY TIMED",
                    BRIGHT_RED, RED, self.time_restricted, 150, 100)
                self.draw.Button(self.WIDTH-350, 2*self.HEIGHT/3, "QUIT", BRIGHT_GREEN, GREEN, quit, 150, 100)
                self.draw.draw_text("Your Score : %d" % (self.score), self.WIDTH/2, self.HEIGHT/3, 100, BLUE)
                self.draw.draw_text("HIGH SCORE:%d" % (self.highscore), self.WIDTH-400, 50, 30, BLACK)
                if self.score == self.highscore:
                    self.draw.draw_text("Congratulations you have a new high score",
                        self.WIDTH/2, self.HEIGHT-200, 60, BRIGHT_GREEN)
                pygame.display.flip()
                self.clock.tick(FPS)

    def reload(self) :
        self.misses = 0
        self.highscore = 0
        self.score = 0
        self.last_arrow_time = 0

        # Only for time restricted mode
        if self.time_restricted_mode == True:
            self.remaining_time = GAME_TIME # Remaining time
            self.dt = 0

        self.all_sprites = None
        self.baloons = None
        self.arrows = None
        self.new_baloon = None
        self.new_arrow = None
        self.last_arrow = None
        self.last_baloon_time = 0
        self.last_arrow_time = 0

    def gameloop(self):
        self.reload()
        self.readHighScore()        

        self.all_sprites = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()
        self.baloons = pygame.sprite.Group()

        self.new_arrow = Arrow(self)
        self.all_sprites.add(self.new_arrow)
        self.arrows.add(self.new_arrow)
        self.last_arrow = self.new_arrow

        self.new_baloon = Baloon(self)
        self.all_sprites.add(self.new_baloon)
        self.baloons.add(self.new_baloon)

        # last_arrow_time = pygame.time.get_ticks()
        self.last_baloon_time = pygame.time.get_ticks()
        running = True
#         self.instruction_screen()
        while running:

            self.dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Only for time restricted mode
            if self.time_restricted_mode == True:
                if self.remaining_time <= 0:
                    self.time_restricted_mode = False
                    self.replay()
                self.remaining_time -= self.dt / 1000
            # Only for normal mode
            elif self.misses >= MISSES:
                self.replay()

            now = pygame.time.get_ticks()
            if self.last_arrow.Released and now-self.last_arrow_time > 1000:
                self.new_arrow = Arrow(self)
                self.all_sprites.add(self.new_arrow)
                self.arrows.add(self.new_arrow)
                self.last_arrow = self.new_arrow
                # last_arrow_time=now

            if now - self.last_baloon_time > 2000:
                self.new_baloon = Baloon(self)
                self.all_sprites.add(self.new_baloon)
                self.baloons.add(self.new_baloon)
                self.last_baloon_time = now

            for baloon in self.baloons:
                hits = pygame.sprite.spritecollide(
                    baloon, self.arrows, False, pygame.sprite.collide_circle)
                if hits:
                    baloon.kill()
                    explo = Explosion(baloon.rect.center, 100,self)
                    self.all_sprites.add(explo)
                    self.score += 1

                if (self.score > self.highscore):
                    self.highscore = self.score

            self.all_sprites.update()

            self.game_screen()
            pygame.display.flip()

    def game_screen(self) :
        self.screen.fill(SKY_BLUE)
        self.screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(self.screen)
        self.draw.Button(self.WIDTH-120, 20, "PAUSE", BRIGHT_GREEN,
                GREEN, self.pause_function, 100, 100)
        self.draw.Button(self.WIDTH-120, 140, "Instructions", BRIGHT_GREEN,
                GREEN, self.instruction_screen, 100, 100)
        self.draw.Button(self.WIDTH-120, 260, "QUIT", BRIGHT_RED, RED, quit, 100, 100)
        self.draw.Button(self.WIDTH-120, 380, "RESTART", BLUE, SKY_BLUE, self.gameloop, 100, 100)
        self.draw.draw_text("SCORE : %d" % (self.score), self.WIDTH-200, self.HEIGHT-100, 40, BLUE)
        self.draw.draw_text("HIGH SCORE : %d" % (self.highscore),
                self.WIDTH-200, self.HEIGHT-50, 40, BLUE)

        # Display time left, only for time restricted mode
        if self.time_restricted_mode == True:
            if self.remaining_time < 10:
                timer_color = RED
            else:
                timer_color = BLACK
            self.draw.draw_text("TIME LEFT : %d" % (math.ceil(self.remaining_time)),
                self.WIDTH/2, 40, 40, timer_color)
        # Display number of misses, only for normal mode.
        else:
            self.draw.draw_text("MISSES : %d" % (self.misses), self.WIDTH -
                200, self.HEIGHT-150, 50, BRIGHT_RED)

   #screen when instruction button is clicked
    def instruction_screen(self):
        self.instruction = True
        while self.instruction:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                    
                self.screen.fill(SKY_BLUE)
                self.screen.blit(self.background, self.background_rect)    
                self.draw.DrawRect(150,150,self.WIDTH-300,self.HEIGHT-300,GREEN_YELLOW) 
                x=600
                y=300
                self.draw.draw_text("Instructions",self.WIDTH/2,y-100,80,BLACK)
                self.draw.draw_text("1. Use mouse to direct the arrow.",x,y,60,BLACK)
                self.draw.draw_text("2. Click on the arrow to shoot.",x-27,y+80,60,BLACK)
                self.draw.draw_text("3. Drag the arrow to increase velocity",x+50,y+160,60,BLACK)
                self.draw.draw_text(" and then release to shoot.",x-20,y+220,60,BLACK)
                self.draw.Button(self.WIDTH/3, 2*self.HEIGHT/3+self.HEIGHT/20, "RESUME",DARK_BROWN,BROWN,self.resume, 150, 50)
                pygame.display.flip()
                self.clock.tick(FPS)
                
   #function to resume the game             
    def resume(self):
        self.instruction=False

#Class to draw text and surfaces on screen
class Draw() :
    def __init__(self,game) :
        self.game = game

    def DrawRect(self,x, y, w, h, c):
        pygame.draw.rect(self.game.screen, c, [x, y, w, h])

    def text_objects(self,text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()


    def draw_text(self,text, x, y, s, color):
        font_name = pygame.font.match_font('comicsansms.ttf')
        s = int(s)
        largeText = pygame.font.Font(font_name, s)
        TextSurf, TextRect = self.text_objects(text, largeText, color)
        TextRect.center = ((x, y))
        self.game.screen.blit(TextSurf, TextRect)


    def Button(self,x,y , string, color2, color1, function, w, h):
        y = int(y) 
        self.game.mouse = pygame.mouse.get_pos()
        self.game.click = pygame.mouse.get_pressed()
        self.DrawRect(x, y, w, h, color1)
        if x <= self.game.mouse[0] <= x+w and y <= self.game.mouse[1] <= y+h:
            self.DrawRect(x, y, w, int(h), color2)
            if (self.game.click[0] == 1):
                self.game.select_sound.play()
                function()
        self.draw_text(string, x+w/2, y+h/2, (w+h)/8, BLACK)
        
    
