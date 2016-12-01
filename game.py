#!/usr/bin/env python
# -*- coding: utf-8 -*-



import random
import sys

import pygame
from pygame import *
from pygame.sprite import *

X_MAX = 800
Y_MAX = 600

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1

everything = pygame.sprite.Group()

class PokeballSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(PokeballSprite, self).__init__()
        self.image = pygame.image.load("Pokeball.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y-10)

    def update(self):
        x, y = self.rect.center
        y -= 15
        self.rect.center = x, y
        if y <= 0:
            self.kill()


class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, x_pos, groups):
        super(EnemySprite, self).__init__()
        self.image = pygame.image.load("Pikachu.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, 0)

        self.velocity = random.randint(3, 10)

        self.add(groups)
        # self.explosion_sound = pygame.mixer.Sound("Arcade Explo A.wav")
        # self.explosion_sound.set_volume(0.4)

    def update(self):
        x, y = self.rect.center

        if y > Y_MAX:
            x, y = random.randint(0, X_MAX), 0
            self.velocity = random.randint(3, 10)
        else:
            x, y = x, y + self.velocity

        self.rect.center = x, y

    def kill(self):
        x, y = self.rect.center
        # if pygame.mixer.get_init():
        # self.explosion_sound.play(maxtime=1000)
        # Explosion(x, y)
        super(EnemySprite, self).kill()


class StatusSprite(pygame.sprite.Sprite):
    def __init__(self, ship, groups):
        super(StatusSprite, self).__init__()
        self.image = pygame.Surface((X_MAX, Y_MAX))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = 0, Y_MAX

        default_font = pygame.font.get_default_font()
        self.font = pygame.font.Font(default_font, 20)

        self.ship = ship
        self.add(groups)

    def update(self):
        score = self.font.render("Health : {} Score : {}".format(
            self.ship.health, self.ship.score), True, (150, 50, 50))
        self.image.fill((0, 0, 0))
        self.image.blit(score, (0, 0))


class ShipSprite(pygame.sprite.Sprite):
    def __init__(self, groups, weapon_groups):
        super(ShipSprite, self).__init__()
        self.image = pygame.image.load("Ash_Ketchum.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (X_MAX/2, Y_MAX - 10)
        self.dx = self.dy = 0
        self.firing = self.shot = False
        self.health = 100
        self.score = 0

        self.groups = [groups, weapon_groups]

        self.mega = 1

        self.autopilot = False
        self.in_position = False
        self.velocity = 2

    def update(self):
        x, y = self.rect.center

        if not self.autopilot:
            # Handle movement
            self.rect.center = x + self.dx, y + self.dy

            # Handle firing
            if self.firing:
                self.shot = PokeballSprite(x, y)
                self.shot.add(self.groups)

            if self.health < 0:
                self.kill()
        else:
            if not self.in_position:
                if x != X_MAX/2:
                    x += (abs(X_MAX/2 - x)/(X_MAX/2 - x)) * 2
                if y != Y_MAX - 100:
                    y += (abs(Y_MAX - 100 - y)/(Y_MAX - 100 - y)) * 2

                if x == X_MAX/2 and y == Y_MAX - 100:
                    self.in_position = True
            else:
                y -= self.velocity
                self.velocity *= 1.5
                if y <= 0:
                    y = -30
            self.rect.center = x, y

    def steer(self, direction, operation):
        v = 10
        if operation == START:
            if direction in (UP, DOWN):
                self.dy = {UP: -v,
                           DOWN: v}[direction]

            if direction in (LEFT, RIGHT):
                self.dx = {LEFT: -v,
                           RIGHT: v}[direction]

        if operation == STOP:
            if direction in (UP, DOWN):
                self.dy = 0
            if direction in (LEFT, RIGHT):
                self.dx = 0

    def shoot(self, operation):
        if operation == START:
            self.firing = True
        if operation == STOP:
            self.firing = False

def main():
    game_over = False
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((X_MAX, Y_MAX))
    enemies = pygame.sprite.Group()
    weapon_fire = pygame.sprite.Group()

    empty = pygame.Surface((X_MAX, Y_MAX))
    clock = pygame.time.Clock()

    ship = ShipSprite(everything, weapon_fire)
    ship.add(everything)

    status = StatusSprite(ship, everything)

    deadtimer = 30
    credits_timer = 250

    for i in range(10):
        pos = random.randint(0, X_MAX)
        EnemySprite(pos, [everything, enemies])

    # # Get some music
    # if pygame.mixer.get_init():
    #     pygame.mixer.music.load("DST-AngryMod.mp3")
    #     pygame.mixer.music.set_volume(0.8)
    #     pygame.mixer.music.play(-1)

    while True:
        clock.tick(30)
        # Check for input
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
                break
            if not game_over:
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        ship.steer(DOWN, START)
                    if event.key == K_LEFT:
                        ship.steer(LEFT, START)
                    if event.key == K_RIGHT:
                        ship.steer(RIGHT, START)
                    if event.key == K_UP:
                        ship.steer(UP, START)
                    if event.key == K_LCTRL:
                        ship.shoot(START)
                    if event.key == K_RETURN:
                        if ship.mega:
                            ship.mega -= 1
                            for i in enemies:
                                i.kill()

                if event.type == KEYUP:
                    if event.key == K_DOWN:
                        ship.steer(DOWN, STOP)
                    if event.key == K_LEFT:
                        ship.steer(LEFT, STOP)
                    if event.key == K_RIGHT:
                        ship.steer(RIGHT, STOP)
                    if event.key == K_UP:
                        ship.steer(UP, STOP)
                    if event.key == K_LCTRL:
                        ship.shoot(STOP)

        # Check for impact
        hit_ships = pygame.sprite.spritecollide(ship, enemies, True)
        for i in hit_ships:
            ship.health -= 15

        if ship.health < 0:
            if deadtimer:
                deadtimer -= 1
            else:
                #sys.exit()
                game_over = True

        # Check for successful attacks
        hit_ships = pygame.sprite.groupcollide(
            enemies, weapon_fire, True, True)
        for k, v in hit_ships.items():
            k.kill()
            for i in v:
                i.kill()
                ship.score += 10

        if len(enemies) < 20 and not game_over:
            pos = random.randint(0, X_MAX)
            EnemySprite(pos, [everything, enemies])

        # Check for game over
        if ship.score > 1000:
            game_over = True
            for i in enemies:
                i.kill()

            ship.autopilot = True
            ship.shoot(STOP)

        if game_over:
            # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
            myfont = pygame.font.SysFont("monospace", 15)

            # render text
            label = myfont.render("Game Over!", 1, (255,255,0))
            screen.blit(label, (100, 100))
            #pygame.mixer.music.fadeout(8000)
            # for i in stars:
            #     i.accelerate()
            if credits_timer:
                credits_timer -= 1
            else:
                sys.exit()

        # Update sprites
        everything.clear(screen, empty)
        everything.update()
        everything.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
