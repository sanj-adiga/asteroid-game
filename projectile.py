import pygame
from settings import PROJECTILE_SPEED, PROJECTILE_SIZE
from pymunk import Vec2d
import os

class Projectile:
    def __init__(self, x, y):
        self.position = Vec2d(x, y)
        self.velocity = Vec2d(0, -PROJECTILE_SPEED)

        projectile_img_path = os.path.join("assets", "projectile.png")
        self.image = pygame.image.load(projectile_img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (PROJECTILE_SIZE, PROJECTILE_SIZE))
        self.rect = self.image.get_rect()

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.topleft = (int(self.position.x), int(self.position.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
