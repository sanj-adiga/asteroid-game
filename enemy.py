# enemy.py

import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from pymunk import Vec2d

# load enemy sprites
attack = [pygame.image.load("assets/basic_enemy_sprites/Attack_1.png"),
          pygame.image.load("assets/basic_enemy_sprites/Attack_2.png")]
boost = [pygame.image.load("assets/basic_enemy_sprites/Boost.png")]
charge = [pygame.image.load("assets/basic_enemy_sprites/Charge_1.png"),
          pygame.image.load("assets/basic_enemy_sprites/Charge_2.png")]
damage = [pygame.image.load("assets/basic_enemy_sprites/Damage.png")]
destroyed = [pygame.image.load("assets/basic_enemy_sprites/Destroyed.png")]
evasion = [pygame.image.load("assets/basic_enemy_sprites/Evasion.png")]
idle = [pygame.transform.rotate(pygame.image.load("assets/basic_enemy_sprites/move_animations/move1.png"), 270) ,pygame.transform.rotate(pygame.image.load("assets/basic_enemy_sprites/move_animations/move2.png"), 270),pygame.transform.rotate(pygame.image.load("assets/basic_enemy_sprites/move_animations/move3.png"), 270),pygame.transform.rotate(pygame.image.load("assets/basic_enemy_sprites/move_animations/move4.png"), 270),pygame.transform.rotate(pygame.image.load("assets/basic_enemy_sprites/move_animations/move5.png"), 270),pygame.transform.rotate(pygame.image.load("assets/basic_enemy_sprites/move_animations/move6.png"), 270)]
move = [pygame.image.load("assets/basic_enemy_sprites/Move.png")]
turn = [pygame.image.load("assets/basic_enemy_sprites/Turn_1.png"),
        pygame.image.load("assets/basic_enemy_sprites/Turn_2.png")]


class Enemy:
    def __init__(self, x, y, speed=20, health=1, shoot_interval=4, color=(255, 0, 0), pattern="straight"):
        self.position = Vec2d(x, y)
        self.speed = speed
        self.health = health
        self.size = 40
        self.shape = pygame.Rect(self.position.x, self.position.y, self.size, self.size)
        self.projectiles = []
        self.shoot_timer = 0
        self.shoot_interval = shoot_interval
        self.color = color
        self.pattern = pattern
        self.direction = Vec2d(0, 1)
        self.change_direction_interval = 3
        self.direction_timer = 0

        self.animations = {
            "attack": attack,
            "boost": boost,
            "charge": charge,
            "damage": damage,
            "destroyed": destroyed,
            "evasion": evasion,
            "idle": idle,
            "move": move,
            "turn": turn
        }

        self.current_animation = "idle"
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_duration = 0.1

    def update(self, dt):
        self.move(dt)
        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_interval:
            self.shoot()
            self.shoot_timer = 0

        self.frame_timer += dt
        if self.frame_timer >= self.frame_duration:
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_animation])
            self.frame_timer = 0

        for proj in self.projectiles[:]:
            proj.update(dt)
            if proj.position.y > SCREEN_HEIGHT:
                self.projectiles.remove(proj)

    def move(self, dt):
        self.direction_timer += dt
        if self.direction_timer >= self.change_direction_interval:
            self.change_direction()
            self.direction_timer = 0

        max_y_position = SCREEN_HEIGHT * 0.3 - self.size

        movement = self.direction * self.speed * dt
        new_position = self.position + movement

        if 0 <= new_position.x <= SCREEN_WIDTH - self.size - 10 and 0 <= new_position.y <= max_y_position:
            self.position = new_position
        else:
            self.change_direction()

        self.shape.topleft = (self.position.x, self.position.y)

    def change_direction(self):
        angle = random.uniform(0, 360)
        self.direction = Vec2d(1, 0).rotated_degrees(angle)

    def draw(self, screen):
        current_frame = self.animations[self.current_animation][self.frame_index]
        screen.blit(current_frame, (self.position.x, self.position.y))

        for proj in self.projectiles:
            proj.draw(screen)

    def shoot(self):
        projectile_x = self.position.x + self.size // 2 + 76
        projectile_y = self.position.y + self.size  + 80 # front edge of the enemy

        self.projectiles.append(
            EnemyProjectile(projectile_x, projectile_y, Vec2d(0, 200)))

class EnemyProjectile:
    def __init__(self, x, y, velocity=Vec2d(0, 200), size=40):
        self.position = Vec2d(x, y)
        self.velocity = velocity
        self.size = size
        self.image = pygame.image.load("assets/Charge_2.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image = pygame.transform.rotate(self.image, 90)


    def update(self, dt):
        self.position += self.velocity * dt

    def draw(self, screen):
        screen.blit(self.image, (int(self.position.x), int(self.position.y)))


class EnemyManager:
    def __init__(self):
        self.enemies = []

    def spawn_enemy(self, x, y, enemy_type="basic"):
        if enemy_type == "basic":
            enemy = Enemy(x, y, speed=100, health=1, shoot_interval=1.5, color=(255, 0, 0), pattern="straight")
        elif enemy_type == "zigzag":
            enemy = Enemy(x, y, speed=80, health=2, shoot_interval=2, color=(0, 255, 0), pattern="zigzag")
        elif enemy_type == "spread":
            enemy = Enemy(x, y, speed=60, health=3, shoot_interval=1, color=(0, 0, 255), pattern="spread")
        self.enemies.append(enemy)

    def update(self, dt):
        for enemy in self.enemies[:]:
            enemy.update(dt)
            if enemy.position.y > SCREEN_HEIGHT or enemy.health <= 0:
                self.enemies.remove(enemy)

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
