import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from pymunk import Vec2d

class Ammo:
    def __init__(self, y_speed=100, size=60):
        # initialzie ammo with random x position at top of screen
        self.position = Vec2d(random.randint(0, SCREEN_WIDTH - size), 0)
        self.y_speed = y_speed  # Falling speed
        self.size = size
        #  scale ammo
        self.image = pygame.image.load("assets/ammo.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def update(self, dt):
        self.position += Vec2d(0, self.y_speed * dt)

    def draw(self, screen):
        screen.blit(self.image, (int(self.position.x), int(self.position.y)))

    def is_off_screen(self):
        return self.position.y > SCREEN_HEIGHT

    def check_collision(self, player_rect):
        ammo_rect = pygame.Rect(self.position.x, self.position.y, self.size, self.size)
        return ammo_rect.colliderect(player_rect)

class AmmoManager:
    def __init__(self):
        self.ammos = []

    def spawn_ammo(self):
        self.ammos.append(Ammo())

    def update(self, dt, player_rect):
        for ammo in self.ammos[:]:
            ammo.update(dt)
            # check if ammo collides with the player
            if ammo.check_collision(player_rect):
                self.ammos.remove(ammo)
                return True  # indicate that ammo was collected
        return False  # no collision

    def draw(self, screen):
        for ammo in self.ammos:
            ammo.draw(screen)
