import pygame
from explosion import Explosion
from settings import PLAYER_SIZE, ASTEROID_SIZE, PROJECTILE_SIZE


def detect_collisions(player, asteroids, projectiles, enemies, explosions, enemy_hitbox):
    player_rect = pygame.Rect(player.position.x, player.position.y, PLAYER_SIZE, PLAYER_SIZE)

    destroyed_asteroids = []
    destroyed_enemies = []

    # check for collisions between player and asteroids
    for asteroid in asteroids[:]:
        asteroid_rect = pygame.Rect(asteroid.position.x, asteroid.position.y, ASTEROID_SIZE, ASTEROID_SIZE)
        if player_rect.colliderect(asteroid_rect):
            player.health -= 10
            if asteroid in asteroids:
                asteroids.remove(asteroid)
                explosion = Explosion(asteroid.position.x, asteroid.position.y)
                explosions.append(explosion)
                print(f"Player hit by asteroid! Health: {player.health}")

    # check for collisions between player projectiles and asteroids
    for asteroid in asteroids[:]:
        for projectile in projectiles[:]:
            distance = asteroid.position.get_distance(projectile.position)
            if distance <= asteroid.hitbox_radius + (PROJECTILE_SIZE / 2):
                try:
                    projectiles.remove(projectile)
                    if asteroid in asteroids:
                        asteroids.remove(asteroid)
                        destroyed_asteroids.append(asteroid)
                        explosion = Explosion(asteroid.position.x, asteroid.position.y)
                        explosions.append(explosion)
                        print("Asteroid destroyed!")
                except ValueError:
                    pass  # Ignore if already removed
                break

    # check for collisions between player and enemy projectiles
    for enemy in enemies.enemies[:]:
        for enemy_proj in enemy.projectiles[:]:
            enemy_proj_rect = pygame.Rect(enemy_proj.position.x, enemy_proj.position.y, enemy_proj.size,
                                          enemy_proj.size)
            if player_rect.colliderect(enemy_proj_rect):
                player.health -= 5
                try:
                    enemy.projectiles.remove(enemy_proj)
                    print(f"Player hit by enemy projectile! Health: {player.health}")
                except ValueError:
                    pass

    # check for collisions between player projectiles and enemies
    for enemy in enemies.enemies[:]:

        # define the enemy hitbox rectangle
        enemy_rect = pygame.Rect(enemy.position.x + enemy.size/2 + 57, enemy.position.y + enemy.size + 30, enemy.size, enemy.size)

        enemy_rect = pygame.Rect(enemy.position.x + enemy.size / 2 + 57, enemy.position.y + enemy.size + 80, enemy.size,
                                 enemy.size)

        enemy_hitbox.append(enemy_rect)

        for projectile in projectiles[:]:
            projectile_rect = pygame.Rect(projectile.position.x, projectile.position.y, 5, 5)
            if enemy_rect.colliderect(projectile_rect):
                enemy.health -= 1
                try:
                    projectiles.remove(projectile)
                    explosion = Explosion(enemy.position.x, enemy.position.y)
                    explosions.append(explosion)
                    print("Enemy hit by projectile!")
                except ValueError:
                    pass

                if enemy.health <= 0:
                    try:
                        enemies.enemies.remove(enemy)
                        destroyed_enemies.append(enemy)
                        print("Enemy destroyed!")
                    except ValueError:
                        pass
                break
# return values for scoring purposes
    return destroyed_asteroids, destroyed_enemies
