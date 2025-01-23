# settings.py

import pygame
pygame.init()



FULLSCREEN = True


if FULLSCREEN:
    SCREEN_WIDTH = pygame.display.Info().current_w
    SCREEN_HEIGHT = pygame.display.Info().current_h
    SCREEN_MODE = pygame.FULLSCREEN
else:
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    SCREEN_MODE = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLAYER_SIZE = 120
PLAYER_SPEED = 500
PLAYER_HEALTH = 100
PLAYER_AMMO = 100

PROJECTILE_SPEED = 400
PROJECTILE_SIZE = 25

ASTEROID_SIZE = 30
ASTEROID_SPEED = 200

GRAVITY = (0, 0)

clock = pygame.time.Clock()
