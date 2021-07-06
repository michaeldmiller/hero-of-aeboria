# Hero of Aeboria, version 0.0.1
# changelog: with a strong base engine with (at least mostly) working physics,
# we can now officially switch to git managed versioning and officially leave experimental builds behind.

# officially naming version on github

# import modules
import pygame
from pygame.locals import *
import os
import sys
import random

vec = pygame.math.Vector2

# important constants and variables

target_frame_rate = 60
window_x_size = 1000
window_y_size = 500
terrain_list = [(500, 400, 5000, 20), (300, 350, 100, 50), (500, 325, 100, 50), (700, 300, 100, 50),
                (900, 300, 200, 50), (1100, 300, 50, 500), (-200, 310, 350, 50), (-210, 315, 100, 75),
                (-260, 350, 30, 50)]
gravity = 0.35
friction_constant = -0.07
side_scroll_speed = 1

# speed = how many seconds should elapse, on average,
# between two new terrain pieces spawning
terrain_gen_speed = 2


# initialize pygame

# loading function definitions


class Game:
    """Class to initialize and hold game loop, handle events, and manage collisions"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((window_x_size, window_y_size))
        pygame.display.set_caption("Experiment 1")
        self.clock = pygame.time.Clock()
        self.new_game()
        self.background = True

    def new_game(self):
        self.frame_count = 1
        self.all_sprites = pygame.sprite.Group()
        self.terrain = pygame.sprite.Group()
        self.hero = Hero(self)
        self.all_sprites.add(self.hero)
        self.background = load_image("banner.jpg")
        self.background = self.background[0].convert()
        self.font = pygame.font.SysFont("cambria.ttf", 20)
        self.text_surface = self.font.render(str(self.hero.velocity), False, (0, 0, 0))
        for terrain_tuple in terrain_list:
            x_val = terrain_tuple[0]
            y_val = terrain_tuple[1]
            w_val = terrain_tuple[2]
            h_val = terrain_tuple[3]
            terrain_piece = TerrainElement(x_val, y_val, w_val, h_val)
            self.all_sprites.add(terrain_piece)
            self.terrain.add(terrain_piece)
        # self.first_sound = load_sound('1.wav')
        # self.second_sound = load_sound('2.wav')

        self.run()

    def run(self):
        while True:
            # delta_time = self.clock.tick(60) * 0.001 * target_frame_rate
            self.clock.tick(target_frame_rate)
            self.frame_count += 1
            if self.frame_count > target_frame_rate:
                self.frame_count = 1
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

        # detect collisions
        collision = pygame.sprite.spritecollide(self.hero, self.terrain, False)
        if collision:
            if len(collision) == 1:
                # old interpretation: if collision[0].rect.y > self.hero.rect.y:
                # within 15 pixels or if character is falling at greater than 15 px/sec (i.e. could
                # get more than 15 px into the object in less than 1 frame)
                if abs(collision[0].rect.y - self.hero.rect.bottom) < 15 or self.hero.velocity.y > 15:
                    # above
                    self.hero.position.y = collision[0].rect.top + 1
                    self.hero.velocity.y = 0
                    self.hero.on_ground = True
                elif abs(collision[0].rect.left - self.hero.rect.right) < 5:
                    # left
                    self.hero.position.x = collision[0].rect.left - (0.5 * self.hero.rect.width)
                    self.hero.velocity.x = 0
                elif abs(collision[0].rect.right - self.hero.rect.left) < 5:
                    # right
                    self.hero.position.x = collision[0].rect.right + (0.5 * self.hero.rect.width)
                    self.hero.velocity.x = 0
                elif collision[0].rect.bottom > self.hero.rect.top:
                    # below
                    # bounce back with equivalent or a maximum y velocity
                    if abs(self.hero.velocity.y) > 0:
                        if abs(self.hero.velocity.y) > 1:
                            self.hero.velocity.y = 1
                        else:
                            self.hero.velocity.y = - self.hero.velocity.y
                    else:
                        self.hero.velocity.y = 0
                    # set position to bottom and set acceleration to gravity
                    self.hero.position.y = collision[0].rect.bottom + self.hero.rect.height + 1
                    self.hero.on_ground = False
                    self.hero.acceleration.y = gravity

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
                if collision[location_of_lowest].rect.y > self.hero.rect.y:
                        self.hero.position.y = collision[location_of_lowest].rect.top + 1
                        self.hero.velocity.y = 0
                        self.hero.on_ground = True
                        # print("top")

                # then remove the ground object and calculate directional collisions
                new_collision = list(collision)
                del new_collision[location_of_lowest]
                for remaining in new_collision:
                    if abs(remaining.rect.left - self.hero.rect.right) < 5:
                        # left
                        self.hero.position.x = remaining.rect.left - (0.5 * self.hero.rect.width)
                        self.hero.velocity.x = 0
                    elif abs(remaining.rect.right - self.hero.rect.left) < 5:
                        # right
                        self.hero.position.x = remaining.rect.right + (0.5 * self.hero.rect.width)
                        self.hero.velocity.x = 0
                    elif remaining.rect.bottom > self.hero.rect.top:
                        # below
                        # bounce back with equivalent or a maximum y velocity
                        if abs(self.hero.velocity.y) > 0:
                            if abs(self.hero.velocity.y) > 1:
                                self.hero.velocity.y = 1
                            else:
                                self.hero.velocity.y = - self.hero.velocity.y
                        else:
                            self.hero.velocity.y = 0
                        # set position to bottom and set acceleration to gravity
                        self.hero.position.y = remaining.rect.bottom + self.hero.rect.height + 1
                        self.hero.on_ground = False
                        self.hero.acceleration.y = gravity

            # self.hero.rect.midbottom = self.hero.position

        # if no collision, apply gravity
        if not collision:
            self.hero.acceleration.y = gravity

        # screen recenter
        if self.hero.position.x > 0.93 * window_x_size:
            self.hero.position.x -= 5
            for block in self.terrain:
                block.position.x -= 5

        if self.hero.position.x < 0.07 * window_x_size:
            self.hero.position.x += 5
            for block in self.terrain:\
                block.position.x += 5

        self.side_scroll()

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        text_surface = self.font.render(str(self.hero.velocity) + str(self.hero.acceleration)
                                        + str(mouse_pos) + str(self.hero.position) + str(self.hero.time_since_jump), True, (0, 0, 0))
        collision = pygame.sprite.spritecollide(self.hero, self.terrain, False)
        collision_text = ""
        for all in collision:
            collision_text += "X: " + str(all.rect.x) + " Y: " + str(all.rect.y) + "; "
        collision_text_surface = self.font.render(collision_text, True, (0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(text_surface, (40, 50))
        self.screen.blit(collision_text_surface, (40, 75))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def side_scroll(self):
        pass
        # if self.frame_count == 1:
        #     new_terrain_piece = TerrainElement(window_x_size, random.randint(0, window_y_size),
        #                                        random.randint(30, 400), random.randint(10, 50))
        #     self.all_sprites.add(new_terrain_piece)
        #     self.terrain.add(new_terrain_piece)

        #
        # # randomly add new terrain pieces
        # if random.randint(0, terrain_gen_speed * target_frame_rate) == terrain_gen_speed * target_frame_rate:
        #     new_terrain_piece = TerrainElement(window_x_size, random.randint(0, window_y_size),
        #                                        random.randint(30, 400), random.randint(10, 50))
        #     self.all_sprites.add(new_terrain_piece)
        #     self.terrain.add(new_terrain_piece)

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            # elif event.type == MOUSEBUTTONDOWN:
            #     self.first_sound.play()


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
        self.time_since_jump = 0
        self.cant_go_right = False
        self.cant_go_left = False

    def update(self):
        """hero movement and position instructions"""
        # initial variable settings
        self.acceleration.x = 0
        self.going_left = False
        self.going_right = False
        keys = pygame.key.get_pressed()
        self.time_since_jump += 1

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

        # check if the player is trying to go left or right
        if keys[K_LEFT] and not keys[K_RIGHT]:
            self.going_left = True

        if keys[K_RIGHT] and not keys[K_LEFT]:
            self.going_right = True

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
            for terrain_piece in self.game.terrain:
                terrain_piece.position.x -= self.velocity.x + (0.5 * self.acceleration.x)
            if self.going_left:
                self.position.x += self.velocity.x + (0.5 * self.acceleration.x)
            self.position.y += self.velocity.y + (0.5 * self.acceleration.y)

        # ibid for left edge
        elif self.at_left_edge:
            self.acceleration.x += self.velocity.x * friction_constant
            self.velocity += self.acceleration
            for terrain_piece in self.game.terrain:
                terrain_piece.position.x -= self.velocity.x + (0.5 * self.acceleration.x)
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


# thanks pygame tutorials
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


game = Game()
