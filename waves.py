import random
from asteroid import Asteroid
from enemy import EnemyManager
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Waves:
    def __init__(self, enemy_manager, asteroids):
        self.enemy_manager = enemy_manager
        self.asteroids = asteroids
        self.current_wave = 0
        self.wave_active = False
        self.between_waves = False
        self.wave_data = [

            {"enemies": 3, "asteroids": 0, "enemy_type": "basic"},
            {"enemies": 4, "asteroids": 3, "enemy_type": "zigzag"},
            {"enemies": 4, "asteroids": 5, "enemy_type": "spread"},
            {"enemies": 5, "asteroids": 7, "enemy_type": "spread"},

        ]

        self.spawn_timer = 0
        self.spawn_interval = 4

    def start_wave(self, wave_index):
        self.current_wave = wave_index
        self.wave_active = True
        self.between_waves = False
        self.wave_data[self.current_wave]["enemies_left_to_spawn"] = self.wave_data[self.current_wave]["enemies"]
        self.wave_data[self.current_wave]["asteroids_left_to_spawn"] = self.wave_data[self.current_wave]["asteroids"]
        self.spawn_timer = 0

    def update(self, dt):
        if not self.wave_active or self.current_wave >= len(self.wave_data):
            return

        wave_info = self.wave_data[self.current_wave]

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval and wave_info["enemies_left_to_spawn"] > 0:
            enemy_x = random.randint(0, SCREEN_WIDTH - 40)
            self.enemy_manager.spawn_enemy(enemy_x, 0, wave_info["enemy_type"])
            wave_info["enemies_left_to_spawn"] -= 1
            self.spawn_timer = 0

        while wave_info["asteroids_left_to_spawn"] > 0:
            self.asteroids.append(Asteroid())
            wave_info["asteroids_left_to_spawn"] -= 1

        if wave_info["enemies_left_to_spawn"] <= 0 and wave_info["asteroids_left_to_spawn"] <= 0:
            if len(self.enemy_manager.enemies) == 0 and len(self.asteroids) == 0:
                self.wave_active = False
                self.between_waves = True
                print(f"Wave {self.current_wave + 1} complete!")

    def is_wave_active(self):
        return self.wave_active

    def is_between_waves(self):
        return self.between_waves
