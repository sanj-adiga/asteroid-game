import pygame
from settings import PLAYER_SIZE, PLAYER_SPEED, PLAYER_HEALTH, PLAYER_AMMO, SCREEN_WIDTH, SCREEN_HEIGHT, PROJECTILE_SIZE
from projectile import Projectile
from pymunk import Vec2d
import os

class Player:
    def __init__(self):
        #  player properties
        self.position = Vec2d(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE - 10)
        self.shape = pygame.Rect(self.position.x, self.position.y, PLAYER_SIZE, PLAYER_SIZE)
        self.ammo = PLAYER_AMMO
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH

        # load spaceship attack sprites
        self.attack_sprites = []
        self.current_sprite_index = 0
        self.sprite_change_delay = 5  # Adjust this for animation speed
        self.sprite_counter = 0

        # load all sprites from the spaceship_attack directory
        spaceship_attack_path = "assets/spaceship_attack/"
        for i in range(1, 5):
            sprite = pygame.image.load(os.path.join(spaceship_attack_path, f"Attack1{i}.png")).convert_alpha()
            sprite = pygame.transform.scale(sprite, (PLAYER_SIZE, PLAYER_SIZE))
            self.attack_sprites.append(sprite)

        self.default_sprite = self.attack_sprites[0]
        self.current_sprite = self.default_sprite

        #  thruster sprite
        self.thruster_sprite = pygame.image.load("assets/spaceship_boost.png").convert_alpha()
        self.thruster_sprite = pygame.transform.scale(self.thruster_sprite, (PLAYER_SIZE, PLAYER_SIZE))

        # pulse sprite for the power-up effect
        self.pulse_sprite = pygame.image.load("assets/pulse.png").convert_alpha()
        self.pulse_sprite = pygame.transform.scale(self.pulse_sprite, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))  # Larger area for pulse

        # load damage sprites for health flashin'
        self.damage_sprites = [
            pygame.transform.scale(
                pygame.image.load(f"assets/spaceship_damage/damage{i}.png").convert_alpha(),
                (PLAYER_SIZE, PLAYER_SIZE)
            ) for i in range(1, 5)
        ]

        # flag to track if the player is shooting and animating
        self.is_shooting = False

        # flag to track if the player is moving
        self.is_moving = False

        self.flashing = False
        self.flash_count = 0
        self.flash_timer = 0
        self.flash_interval = 0.25  # flasg every 0.25 seconds
        self.last_health_threshold = self.max_health
        self.damage_stage = 0  # track which damage sprite to show next

        # Power-up related properties
        self.is_using_power_up = False
        self.power_up_cooldown = 0
        self.power_up_duration = 2  # power-up lasts 2 seconds

        # shooting peed
        self.shooting_speed_factor = 1
        self.no_ammo_reduction_time = 0
        self.no_ammo_reduction_duration = 3

        #double gun mode pew pew
        self.double_gun_mode = False
        self.double_gun_timer = 0
        self.double_gun_duration = 5

    def move(self, keys, dt):
        move_x = 0
        move_y = 0
        self.is_moving = False

        if keys[pygame.K_LEFT] and self.position.x > 0:
            move_x = -PLAYER_SPEED
            self.is_moving = True
        if keys[pygame.K_RIGHT] and self.position.x < SCREEN_WIDTH - PLAYER_SIZE:
            move_x = PLAYER_SPEED
            self.is_moving = True
        if keys[pygame.K_UP] and self.position.y > 0:
            move_y = -PLAYER_SPEED
            self.is_moving = True
        if keys[pygame.K_DOWN] and self.position.y < SCREEN_HEIGHT - PLAYER_SIZE:
            move_y = PLAYER_SPEED
            self.is_moving = True

        movement = Vec2d(move_x, move_y) * dt
        self.position += movement
        self.shape.topleft = (self.position.x, self.position.y)

        # change to thruster sprite if moving
        if self.is_moving and not self.is_shooting:
            self.current_sprite = self.thruster_sprite
        elif not self.is_moving and not self.is_shooting and not self.flashing:
            self.current_sprite = self.default_sprite

    def draw(self, screen):
        screen.blit(self.current_sprite, self.shape.topleft)

    def update(self, dt, keys):
        if keys[pygame.K_r]:
            if self.no_ammo_reduction_time <= 0:
                self.shooting_speed_factor = 0.5
                self.no_ammo_reduction_time = self.no_ammo_reduction_duration

        if self.no_ammo_reduction_time > 0:
            self.no_ammo_reduction_time -= dt
        else:
            self.shooting_speed_factor = 1

        if keys[pygame.K_g] and not self.double_gun_mode:
            self.double_gun_mode = True
            self.double_gun_timer = 3

        if self.double_gun_mode:
            self.double_gun_timer -= dt
            if self.double_gun_timer <= 0:
                self.double_gun_mode = False

    def shoot(self, projectiles):
        if self.ammo > 0 and not self.is_shooting: #check if double gun is active
            projectile_y = self.position.y - PROJECTILE_SIZE

            if self.double_gun_mode: #left and right projectile for double guns
                left_projectile_x = self.position.x + (self.shape.width // 2) - PROJECTILE_SIZE - 5
                left_projectile = Projectile(left_projectile_x, projectile_y)
                projectiles.append(left_projectile)

                right_projectile_x = self.position.x + (self.shape.width // 2) + 5
                right_projectile = Projectile(right_projectile_x, projectile_y)
                projectiles.append(right_projectile)

            else:
                center_projectile_x = self.position.x + (self.shape.width // 2) - PROJECTILE_SIZE // 2
                center_projectile = Projectile(center_projectile_x, projectile_y)
                projectiles.append(center_projectile)

            self.ammo -= 1
            self.is_shooting = True
            self.current_sprite_index = 0

    def update_shooting_sprite(self):
        if self.is_shooting:
            self.sprite_counter += 1
            if self.sprite_counter >= self.sprite_change_delay:
                self.sprite_counter = 0
                self.current_sprite_index += 1

                if self.current_sprite_index < len(self.attack_sprites):
                    self.current_sprite = self.attack_sprites[self.current_sprite_index]
                else:
                    self.current_sprite = self.default_sprite
                    self.is_shooting = False
                    self.current_sprite_index = 0

    def update_damage_sprite(self, dt):
        current_health = self.health

        if self.health <= 80 - 20 * self.damage_stage:
            self.flashing = True
            self.flash_count = 0
            self.damage_stage += 1


        if self.flashing:
            self.flash_timer += dt


            if self.flash_timer > self.flash_interval:
                if self.flash_count < 6:
                    if self.flash_count % 2 == 0:
                        self.current_sprite = self.damage_sprites[self.damage_stage - 1]
                    else:

                        self.current_sprite = self.default_sprite

                    self.flash_count += 1
                else:
                    self.current_sprite = self.default_sprite
                    self.flashing = False

                self.flash_timer = 0


    def update_power_up(self, dt):
        if self.is_using_power_up:
            self.power_up_cooldown -= dt
            if self.power_up_cooldown <= 0:
                self.is_using_power_up = False
                self.current_sprite = self.default_sprite  # Revert back to normal sprite

    def update(self, dt, keys):

        # press g for double gun
        if keys[pygame.K_g] and not self.double_gun_mode:
            self.double_gun_mode = True
            self.double_gun_timer = self.double_gun_duration

        if self.double_gun_mode:
            self.double_gun_timer -= dt
            if self.double_gun_timer <= 0:
                self.double_gun_mode = False  # end after 5 second
