# this file initializes the various sprites used by the hero-of-aeboria game loop
import pygame
from pygame.locals import *
import os
import random

from hoasettings import *
vec = pygame.math.Vector2


class Hero(pygame.sprite.Sprite):
    """Hero (Player) class to move around the screen"""

    def __init__(self, game):
        # pygame Sprite initializer
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = load_image('blonde_man_64_left.png', (255, 255, 255))
        # load sprite images
        self.left_image, self.left_rect = load_image('blonde_man_64_left.png', (255, 255, 255))
        self.right_image, self.right_rect = load_image('blonde_man_64_right.png', (255, 255, 255))
        # load attack images
        self.left_attack_image, self.left_attack_rect = load_image('blonde_man_attack_left.png', (255, 255, 255))
        self.right_attack_image, self.right_attack_rect = load_image('blonde_man_attack_right.png', (255, 255, 255))
        # set other properties
        self.max_speed = 5
        self.position = vec(300, 100)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, gravity)
        # set boolean behavior/state checks, largely for collision purposes
        self.on_ground = False
        self.at_left_edge = False
        self.at_right_edge = False
        self.going_left = False
        self.going_right = False
        self.cant_go_right = False
        self.cant_go_left = False
        self.stuck = False
        self.hero_attack = False
        self.time_since_jump = 0
        self.time_since_attack = 0


    def update(self):
        """hero movement and position instructions"""
        # initial variable settings
        self.acceleration.x = 0
        self.going_left = False
        self.going_right = False
        keys = pygame.key.get_pressed()
        self.time_since_jump += 1
        self.time_since_attack += 1

        # set default animation
        if self.velocity.x > 0:
            self.image = self.right_image
            self.rect = self.right_rect
        if self.velocity.x <= 0:
            self.image = self.left_image
            self.rect = self.left_rect

        # key press actions
        if keys[K_LEFT]:
            self.move_left()
            self.image = self.left_image
            self.rect = self.left_rect
        if keys[K_RIGHT]:
            self.move_right()
            self.image = self.right_image
            self.rect = self.right_rect
        if keys[K_UP]:
            self.jump()
        if keys[K_DOWN]:
            self.acceleration.y = 20
        if keys[K_SPACE]:
            if self.time_since_attack > 30:
                self.hero_attack = True
                self.time_since_attack = 0
                # determine attack direction and animate accordingly
                if self.image == self.left_image:
                    self.image = self.left_attack_image
                    self.rect = self.left_attack_rect
                elif self.image == self.right_image:
                    self.image = self.right_attack_image
                    self.rect = self.right_attack_rect

        # check if the player is trying to go left or right
        if keys[K_LEFT] and not keys[K_RIGHT]:
            self.going_left = True

        if keys[K_RIGHT] and not keys[K_LEFT]:
            self.going_right = True

        # make attack animation sticky
        if self.time_since_attack < 15:
            if self.image == self.left_image:
                self.image = self.left_attack_image
                self.rect = self.left_attack_rect
            elif self.image == self.right_image:
                self.image = self.right_attack_image
                self.rect = self.right_attack_rect
        else:
            self.hero_attack = False

        # check for global statuses
        # falling
        if self.acceleration.y > 0:
            self.on_ground = False

        # at right edge
        if self.position.x > window_x_size * 0.85:
            self.at_right_edge = True
        else:
            self.at_right_edge = False

        # at left edge
        if self.position.x < window_x_size * 0.15:
            self.at_left_edge = True
        else:
            self.at_left_edge = False

        # motion equations

        # if at right edge, move all non hero objects instead of hero
        # with the hero's movement on the x, preserve hero's gravity
        if self.at_right_edge:
            self.acceleration.x += self.velocity.x * friction_constant
            self.velocity += self.acceleration
            for game_object in self.game.not_hero:
                game_object.position.x -= self.velocity.x + (0.5 * self.acceleration.x)
            if self.going_left:
                self.position.x += self.velocity.x + (0.5 * self.acceleration.x)
            self.position.y += self.velocity.y + (0.5 * self.acceleration.y)

        # ibid for left edge
        elif self.at_left_edge:
            self.acceleration.x += self.velocity.x * friction_constant
            self.velocity += self.acceleration
            for game_object in self.game.not_hero:
                game_object.position.x -= self.velocity.x + (0.5 * self.acceleration.x)
            if self.going_right:
                self.position.x += self.velocity.x + (0.5 * self.acceleration.x)
            self.position.y += self.velocity.y + (0.5 * self.acceleration.y)

        # normal newtonian movement if not near the edge of the screen
        else:
            self.acceleration.x += self.velocity.x * friction_constant
            self.velocity += self.acceleration
            self.position += self.velocity + (0.5 * self.acceleration)

        # cap max speed
        if self.velocity.x > self.max_speed:
            self.velocity.x = self.max_speed
        if self.velocity.x < -self.max_speed:
            self.velocity.x = -self.max_speed

        # y wrap
        if self.position.y > window_y_size:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = window_y_size

        # low speed rounding
        if abs(self.velocity.y) < 0.001:
            self.velocity.y = 0
        if abs(self.velocity.x) < 0.001:
            self.velocity.x = 0

        # finally update position
        self.rect.midbottom = self.position

        enemy_collide = pygame.sprite.spritecollide(self, self.game.enemy_sprites, False)

    def jump(self):
        collide = pygame.sprite.spritecollide(self, self.game.terrain, False)
        if collide and self.on_ground and self.time_since_jump > 0.16 * target_frame_rate:
            self.acceleration.y += -10
            self.time_since_jump = 0

    def move_right(self):
        if not self.cant_go_right:
            if self.at_right_edge:
                self.acceleration.x = 0.4
            elif self.at_left_edge:
                self.acceleration.x = 0.4
                # self.velocity.x += 1
                # self.position.x += 5
            else:
                self.acceleration.x = 0.4
            self.cant_go_left = False

    def move_left(self):
        if not self.cant_go_left:
            if self.at_left_edge:
                self.acceleration.x = -0.4
            elif self.at_right_edge:
                self.acceleration.x = -0.4
                # self.velocity.x -= 1
                # self.position.x -= 5
            else:
                self.acceleration.x = -0.4
            self.cant_go_right = False


class Demon(pygame.sprite.Sprite):
    """Demon enemy class"""

    def __init__(self, game, init_x, init_y):
        # <required package>
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = load_image('demon_left.png', (255, 255, 255))
        # load sprite images
        self.left_image, self.left_rect = load_image('demon_left.png', (255, 255, 255))
        self.right_image, self.right_rect = load_image('demon_right.png', (255, 255, 255))
        # set other properties
        self.max_speed = 1.5
        self.position = vec(init_x, init_y)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, gravity)
        self.stuck = False
        self.on_ground = False
        self.time_since_jump = 0
        # </required package>
        self.vector_distance_from_hero = vec(1000, 1000)
        self.linear_distance_from_hero = 1000
        self.time_since_behavior_change = 0
        self.default_acceleration = vec(0, 0)

    def update(self):
        self.acceleration.x = 0
        self.time_since_jump += 1
        self.time_since_behavior_change += 1

        # calculate distance from hero
        self.vector_distance_from_hero = self.position - self.game.hero.position
        self.linear_distance_from_hero = abs(((self.vector_distance_from_hero[0] ** 2) +
                                              (self.vector_distance_from_hero[1] ** 2)) ** 0.5)

        # chase hero
        # movement logic / AI
        # initial direction
        if self.stuck:
            self.jump()

        if self.time_since_behavior_change > 10:
            self.acceleration = self.default_acceleration
            self.time_since_behavior_change = 0

        if self.time_since_jump > 200:
            self.acceleration.x = 0.2

        # if close to hero, chase him
        if self.linear_distance_from_hero < 300:
            if self.vector_distance_from_hero[0] >= 0:
                self.default_acceleration.x = -0.2
            if self.vector_distance_from_hero[0] < 0:
                self.default_acceleration.x = 0.2

        if self.velocity.x < 0:
            self.image = self.left_image
            self.rect = self.left_rect
        elif self.velocity.x >= 0:
            self.image = self.right_image
            self.rect = self.right_rect

        # on ground check
        if self.acceleration.y > 0:
            self.on_ground = False

        # always newtonian physics
        self.acceleration.x += self.velocity.x * friction_constant
        self.velocity += self.acceleration
        self.position += self.velocity + (0.5 * self.acceleration)

        # cap max speed
        if self.velocity.x > self.max_speed:
            self.velocity.x = self.max_speed
        if self.velocity.x < -self.max_speed:
            self.velocity.x = -self.max_speed

        # y wrap
        if self.position.y > window_y_size:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = window_y_size

        # update position
        self.rect.midbottom = self.position

    def jump(self):
        collide = pygame.sprite.spritecollide(self, self.game.terrain, False)
        if collide and self.on_ground and self.time_since_jump > 0.16 * target_frame_rate:
            self.acceleration.y += -10
            self.time_since_jump = 0


class TerrainElement(pygame.sprite.Sprite):
    """Basic terrain objects to collide with"""

    def __init__(self, platx, platy, platw, plath):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((platw, plath))
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = platx
        self.rect.y = platy
        self.position = vec(platx, platy)

    def update(self):
        self.rect.midbottom = self.position


def load_image(name, colorkey=None):
    full_image_name = os.path.join('data', name)
    print(full_image_name)
    try:
        image = pygame.image.load(full_image_name)
    except pygame.error as message:
        print("Unable to load image ", name, " at ", full_image_name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_only_image(name):
    full_image_name = os.path.join('data', name)
    try:
        image = pygame.image.load(full_image_name)
    except pygame.error as message:
        print("Unable to load image ", name, " at ", full_image_name)
        raise SystemExit(message)
    return image


def load_sound(name):
    full_sound_name = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(full_sound_name)
    except pygame.error as message:
        print("Unable to loud sound ", name, " at ", full_sound_name)
        raise SystemExit(message)
    return sound