#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sys
import pygame
from pygame import *
from pygame.sprite import *

DELAY = 1000;
white = (255,255,255)
X_MAX = 800
Y_MAX = 600

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1

everything = pygame.sprite.Group()

class PokeballSprite(Sprite):
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


class PikachuSprite(Sprite):
    def __init__(self, x_pos, groups):
        super(PikachuSprite, self).__init__()
        self.image = pygame.image.load("Pikachu.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, 0)

        self.velocity = random.randint(3, 10)

        self.add(groups)

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
        super(PikachuSprite, self).kill()

class MewSprite(Sprite):
    def __init__(self):
        super(MewSprite, self).__init__()
        self.image = pygame.image.load("Mew.bmp").convert_alpha()
        self.rect = self.image.get_rect()

    # move mew to a new random location
    def move(self):
        randX = random.randint(0, 500)
        randY = random.randint(0, 300)
        self.rect.center = (randX,randY)

    def kill(self):
    	x, y = self.rect.center
    	super(MewSprite, self).kill()

class StatusSprite(Sprite):
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


class AshSprite(Sprite):
    def __init__(self, groups, weapon_groups):
        super(AshSprite, self).__init__()
        self.image = pygame.image.load("Ash_Ketchum.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (X_MAX/2, Y_MAX - 10)
        self.dx = self.dy = 0
        self.firing = self.shot = False
        self.health = 100
        self.score = 0

        self.groups = [groups, weapon_groups]

        self.mega = 1
        self.in_position = False
        self.velocity = 2

    def update(self):
        x, y = self.rect.center

        # Handle movement
        self.rect.center = x + self.dx, y + self.dy

        # Handle firing
        if self.firing:
            self.shot = PokeballSprite(x, y)
            self.shot.add(self.groups)

        if self.health < 0:
            self.kill()

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
	screen.fill(white)
	display.set_caption('Catch the Pikachus!')
	enemies = pygame.sprite.Group()
	weapon_fire = pygame.sprite.Group()

	empty = pygame.Surface((X_MAX, Y_MAX))
	# empty.fill(white)
	clock = pygame.time.Clock()

	ash = AshSprite(everything, weapon_fire)
	ash.add(everything)
	mew = MewSprite()
	mew.add(everything)
	status = StatusSprite(ash, everything)


	for i in range(10):
	    pos = random.randint(0, X_MAX)
	    PikachuSprite(pos, [everything, enemies])

	game_Exit = False

	time.set_timer(USEREVENT + 1, DELAY)

	while True:
	    clock.tick(30)
	    # Check for input
	    for event in pygame.event.get():
	        if event.type == QUIT:
	            pygame.quit()
	            quit()
	            break

	    if event.type == KEYDOWN:
	        if event.key == K_DOWN:
	            ash.steer(DOWN, START)
	        if event.key == K_LEFT:
	            ash.steer(LEFT, START)
	        if event.key == K_RIGHT:
	            ash.steer(RIGHT, START)
	        if event.key == K_UP:
	            ash.steer(UP, START)
	        if event.key == K_LCTRL:
	            ash.shoot(START)

	    if event.type == KEYUP:
	        if event.key == K_DOWN:
	            ash.steer(DOWN, STOP)
	        if event.key == K_LEFT:
	            ash.steer(LEFT, STOP)
	        if event.key == K_RIGHT:
	            ash.steer(RIGHT, STOP)
	        if event.key == K_UP:
	            ash.steer(UP, STOP)
	        if event.key == K_LCTRL:
	            ash.shoot(STOP)

	    if event.type >= USEREVENT + 1:
	    	mew.move()


	    # Check for impact
	    hit_ash = pygame.sprite.spritecollide(ash, enemies, True)
	    for i in hit_ash:
	        ash.health -= 15

	    if ash.health < 0:
	        if deadtimer:
	            deadtimer -= 1
	        else:
	            game_over = True

	    # Check for successful attacks
	    hit_ships = pygame.sprite.groupcollide(
	        enemies, weapon_fire, True, True)
	    for k, v in hit_ships.items():
	        k.kill()
	        for i in v:
	            i.kill()
	            ash.score += 10

	    caught_mew = pygame.sprite.spritecollide(mew, weapon_fire, True)
	    for i in caught_mew:
	    	ash.score += 20
	    	mew.move()
	    	time.set_timer(USEREVENT + 1, DELAY)



	    if len(enemies) < 5 and not game_over:
	        pos = random.randint(0, X_MAX)
	        PikachuSprite(pos, [everything, enemies])

	    # Check for game over
	    if ash.score > 100:
	        game_over = True

	    if game_over:
	        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
	        myfont = pygame.font.SysFont("monospace", 15)

	        # render text
	        label = myfont.render("Game Over!", 1, (255,255,0))
	        screen.blit(label, (100, 100))
	        if credits_timer:
	            credits_timer -= 1
	        else:
	            sys.exit()
	    
	    # Update sprites
	    # everything.clear(screen, empty)
	    everything.update()
	    everything.draw(screen)
	    display.update()
	    # pygame.surface.fill(white)
	   
	    pygame.display.flip()
	    # screen.fill(white)



if __name__ == '__main__':
    main()
    
