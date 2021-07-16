# this file contains various collision handling functions for hero-of-aeboria
import pygame
from hoasettings import *


def terrain_collision(game):
    # detect collisions
    for character in game.character_sprites:
        character.stuck = False
        collision = pygame.sprite.spritecollide(character, game.terrain, False)
        if collision:
            if len(collision) == 1:
                # old interpretation: if collision[0].rect.y > self.hero.rect.y:
                # within 15 pixels or if character is falling at greater than 15 px/sec (i.e. could
                # get more than 15 px into the object in less than 1 frame)
                if abs(collision[0].rect.y - character.rect.bottom) < 15 or character.velocity.y > 15:
                    # above
                    character.position.y = collision[0].rect.top + 1
                    character.velocity.y = 0
                    character.on_ground = True
                elif abs(collision[0].rect.left - character.rect.right) < 5:
                    # left
                    character.position.x = collision[0].rect.left - (0.5 * character.rect.width)
                    character.velocity.x = 0
                    # fixes jump hyper-acceleration bug
                    character.acceleration.y = gravity
                elif abs(collision[0].rect.right - character.rect.left) < 5:
                    # right
                    character.position.x = collision[0].rect.right + (0.5 * character.rect.width)
                    character.velocity.x = 0
                    # fixes jump hyper-acceleration bug
                    character.acceleration.y = gravity
                elif collision[0].rect.bottom > character.rect.top:
                    # below
                    # bounce back with equivalent or a maximum y velocity
                    if abs(character.velocity.y) > 0:
                        if abs(character.velocity.y) > 1:
                            character.velocity.y = 1
                        else:
                            character.velocity.y = - character.velocity.y
                    else:
                        character.velocity.y = 0
                    # set position to bottom and set acceleration to gravity
                    character.position.y = collision[0].rect.bottom + character.rect.height + 1
                    character.on_ground = False
                    character.acceleration.y = gravity

            # if hero is colliding with more than one terrain object
            if len(collision) > 1:
                location_of_lowest = 0
                lowest_y = 0
                location_counter = 0
                # determine which terrain object is the lowest
                for terrain_item in collision:
                    if terrain_item.rect.top > lowest_y:
                        lowest_y = terrain_item.rect.top
                        location_of_lowest = location_counter
                    location_counter += 1
                # assume it is resting on that object and calculate accordingly
                if collision[location_of_lowest].rect.y > character.rect.y:
                    character.position.y = collision[location_of_lowest].rect.top + 1
                    character.velocity.y = 0
                    character.on_ground = True
                    # print("top")

                # then remove the ground object and calculate directional collisions
                new_collision = list(collision)
                del new_collision[location_of_lowest]
                for remaining in new_collision:
                    if abs(remaining.rect.left - character.rect.right) < 5:
                        # left
                        character.position.x = remaining.rect.left - (0.5 * character.rect.width)
                        character.velocity.x = 0
                        character.stuck = True
                        character.on_ground = True
                    elif abs(remaining.rect.right - character.rect.left) < 5:
                        # right
                        character.position.x = remaining.rect.right + (0.5 * character.rect.width)
                        character.velocity.x = 0
                        character.stuck = True
                        character.on_ground = True
                    elif remaining.rect.bottom > character.rect.top:
                        # below
                        # bounce back with equivalent or a maximum y velocity
                        if abs(character.velocity.y) > 0:
                            if abs(character.velocity.y) > 1:
                                character.velocity.y = 1
                            else:
                                character.velocity.y = - character.velocity.y
                        else:
                            character.velocity.y = 0
                        # set position to bottom and set acceleration to gravity
                        character.position.y = remaining.rect.bottom + character.rect.height + 1
                        character.on_ground = False
                        character.acceleration.y = gravity

            # self.hero.rect.midbottom = self.hero.position

        # if no collision, apply gravity
        if not collision:
            character.acceleration.y = gravity


def enemy_collision(game):
    combat = pygame.sprite.spritecollide(game.hero, game.enemy_sprites, False)
    if combat:
        if len(combat) == 1:
            if game.hero.hero_attack:
                combat[0].kill()
            elif game.hero.invulnerability_time == 0:
                if game.hero.health > 1:
                    # bring in terrain collision logic
                    if abs(combat[0].rect.left - game.hero.rect.right) < 5:
                        # left
                        game.hero.position.x = combat[0].rect.left - (0.5 * game.hero.rect.width)
                        game.hero.velocity.x = 0
                    elif abs(combat[0].rect.right - game.hero.rect.left) < 5:
                        # right
                        game.hero.position.x = combat[0].rect.right + (0.5 * game.hero.rect.width)
                        game.hero.velocity.x = 0
                    # reduce hero health
                    game.hero.health -= 1
                    game.hero.invulnerability_time = 2 * target_frame_rate
            # collision during invulnerability
            elif game.hero.invulnerability_time >= 0:
                if abs(combat[0].rect.left - game.hero.rect.right) < 5:
                    # left
                    game.hero.position.x = combat[0].rect.left - (0.5 * game.hero.rect.width)
                    game.hero.velocity.x = 0
                elif abs(combat[0].rect.right - game.hero.rect.left) < 5:
                    # right
                    game.hero.position.x = combat[0].rect.right + (0.5 * game.hero.rect.width)
                    game.hero.velocity.x = 0

            else:
                game.hero.kill()

        # if more than one enemy
        else:
            if game.hero.hero_attack:
                for enemy in combat:
                    enemy.kill()

            elif game.hero.invulnerability_time == 0:
                if game.hero.health > 1:
                    if abs(combat[0].rect.left - game.hero.rect.right) < 5:
                        # left
                        game.hero.position.x = combat[0].rect.left - (0.5 * game.hero.rect.width)
                        game.hero.velocity.x = 0
                    elif abs(combat[0].rect.right - game.hero.rect.left) < 5:
                        # right
                        game.hero.position.x = combat[0].rect.right + (0.5 * game.hero.rect.width)
                        game.hero.velocity.x = 0
                    # reduce hero health
                    game.hero.health -= 1
                    game.hero.invulnerability_time = 2 * target_frame_rate

            elif game.hero.invulnerability_time >= 0:
                if abs(combat[0].rect.left - game.hero.rect.right) < 5:
                    # left
                    game.hero.position.x = combat[0].rect.left - (0.5 * game.hero.rect.width)
                    game.hero.velocity.x = 0
                elif abs(combat[0].rect.right - game.hero.rect.left) < 5:
                    # right
                    game.hero.position.x = combat[0].rect.right + (0.5 * game.hero.rect.width)
                    game.hero.velocity.x = 0

            else:
                game.hero.kill()



