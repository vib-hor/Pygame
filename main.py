# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 1
# Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
# Project setup

import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.img_dir = path.join(path.dirname(__file__), 'img')
        self.snd_dir = path.join(path.dirname(__file__), 'snd')
        self.font_name = pg.font.match_font(FONT_NAME)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        
        # loading all sound files
        #pg.mixer.music.load(path.join(self.snd_dir, 'Soliloquy.mp3'))
        

        self.player_img = pg.image.load(path.join(self.img_dir, "bowArrow.png"))#.convert()
        self.player_img1 = pg.image.load(path.join(self.img_dir, "bow.png"))
        self.mob_img = pg.image.load(path.join(self.img_dir, "frame-2.png"))#.convert()
        self.arrow_img = pg.image.load(path.join(self.img_dir, "arrow.png"))
        self.mobs = pg.sprite.Group()
        self.arrows = pg.sprite.Group()
        self.player = Player(self)        
        for i in range(5):
            self.newmob()
        self.all_sprites.add(self.player)
        self.run()
    
    def newmob(self):
        mob = Mob(self)
        self.all_sprites.add(mob)
        self.mobs.add(mob)

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        # check to see if a bullet hit a mob
        hits = pg.sprite.groupcollide(self.mobs, self.arrows, True, True, pg.sprite.collide_circle )
        """for hit in hits:
            score += 50 - hit.radius
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.9:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)"""
        for hit in hits:
            now = pg.time.get_ticks()
            self.arrows.update()
            self.newmob()
        self.all_sprites.update()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.shoot()


    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        #self.draw.rect(self.screen,WHITE, self.player.rect, 2)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        # game splash/start screen
        # game splash/start screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Soliloquy.mp3'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
       # self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
