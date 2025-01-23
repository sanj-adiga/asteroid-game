import pygame
import random
from settings import ASTEROID_SIZE, ASTEROID_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from pymunk import Vec2d


class Asteroid:
    def __init__(self, scale_factor=3, animation_speed=0.2):
        # inialize asteroid's pos and speed
        self.position = Vec2d(random.randint(0, SCREEN_WIDTH - ASTEROID_SIZE), 0)
        self.velocity = Vec2d(random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED),
                              random.uniform(ASTEROID_SPEED / 2, ASTEROID_SPEED))

        # sprites
        self.frames = []
        for i in range(1, 15):
            filename = f"assets/asteroids/asteroid{i}.png"
            image = pygame.image.load(filename)
            new_width = int(ASTEROID_SIZE * scale_factor)
            new_height = int(ASTEROID_SIZE * scale_factor)
            scaled_image = pygame.transform.scale(image, (new_width, new_height))
            self.frames.append(scaled_image)

        # animation parameters
        self.current_frame = 0
        self.animation_speed = animation_speed
        self.frame_timer = 0

        #  hitbox radius based on the scaled asteroid size
        self.hitbox_radius = int((ASTEROID_SIZE * scale_factor) / 2)

    def update(self, dt):
        self.position += self.velocity * dt

        # update frame for animation
        self.frame_timer += dt
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        screen.blit(self.frames[self.current_frame], (int(self.position.x), int(self.position.y)))
