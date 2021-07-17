# Hero of Aeboria, version 0.4.4
# changelog: complete collision logic overhaul to fix myriad bugs in the collision system which were causing warps
# seemingly at random. Moved away from absolute values to chained conditional checks for left and right, synchronized
# logic between single and multiple collisions, instituted absolute value checks for bottom collisions, and clarified
# high velocity checks for top collisions.

# import modules
import sys
from hoasprites import *
from hoacollision import *

vec = pygame.math.Vector2

# speed = how many seconds should elapse, on average,
# between two new terrain pieces spawning
# terrain_gen_speed = 2


class Game:
    """Class to initialize and hold game loop and handle events"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((window_x_size, window_y_size))
        pygame.display.set_caption("Hero of Aeboria")
        self.clock = pygame.time.Clock()
        self.new_game()
        self.background = True

    def new_game(self):
        self.frame_count = 1

        # screen_widths = pygame.display.list_modes()
        # print(screen_widths)

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()
        self.terrain = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.not_hero = pygame.sprite.Group()

        # add hero
        self.hero = Hero(self)
        self.all_sprites.add(self.hero)
        self.character_sprites.add(self.hero)

        # add test demons
        demon_list = [Demon(self, 500, 100), Demon(self, 900, 100), Demon(self, 1000, 100)]

        # for no demons:
        # demon_list = []

        for demon in demon_list:
            self.all_sprites.add(demon)
            self.character_sprites.add(demon)
            self.enemy_sprites.add(demon)
            self.not_hero.add(demon)

        # add container heart sprite
        self.heart_sprite = pygame.sprite.Sprite()

        # add heart sprite dictionary
        self.health_dict = {1: load_image('one_heart.png', (255, 255, 255)),
                       2: load_image('two_hearts.png', (255, 255, 255)),
                       3: load_image('three_hearts.png', (255, 255, 255)),
                       4: load_image('four_hearts.png', (255, 255, 255)),
                       5: load_image('five_hearts.png', (255, 255, 255))}

        self.heart_sprite.image, self.heart_sprite.rect = self.health_dict[5]
        self.all_sprites.add(self.heart_sprite)

        # initialize background
        self.background = load_image("mountain_background.png")
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
            self.not_hero.add(terrain_piece)
        # self.first_sound = load_sound('1.wav')
        # self.second_sound = load_sound('2.wav')

        print(self.not_hero)
        # for all in self.not_hero:
        #     print(all)
        #     print(type(all))
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
        terrain_collision(self)
        enemy_collision(self)

        # screen recenter
        if self.hero.position.x > 0.93 * window_x_size:
            self.hero.position.x -= 5
            for element in self.not_hero:
                element.position.x -= 5

        if self.hero.position.x < 0.07 * window_x_size:
            self.hero.position.x += 5
            for element in self.not_hero:
                element.position.x += 5

        self.side_scroll()

    def draw(self):
        # background and diagnostics
        self.screen.blit(self.background, (0, 0))

        # development only
        if self.hero.diagnostic:
            mouse_pos = pygame.mouse.get_pos()
            text_surface = self.font.render(str(self.hero.velocity) + str(self.hero.acceleration)
                                            + str(mouse_pos) + str(self.hero.position) + str(self.hero.time_since_jump),
                                            True, (0, 0, 0))
            collision = pygame.sprite.spritecollide(self.hero, self.terrain, False)
            collision_text = ""
            for all in collision:
                collision_text += "X: " + str(all.rect.x) + " Y: " + str(all.rect.y) + "; "
            collision_text_surface = self.font.render(collision_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (40, 50))
            self.screen.blit(collision_text_surface, (40, 75))

        # damage invulnerability
        if self.hero.invulnerability_time > 0.05:
            invulnerability_text_surface = self.font.render("Damage invulnerability time remaining: " +
                                                            str(round(self.hero.invulnerability_time / target_frame_rate, 1)),
                                                            True, (0, 0, 0))
            self.screen.blit(invulnerability_text_surface, (40, 85))

        # hero health
        self.heart_sprite.image, self.heart_sprite.rect = self.health_dict[self.hero.health]
        self.heart_sprite.rect.x = 40
        self.heart_sprite.rect.y = 25

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


# format for stage block dictionaries:
# name, [course object 1, course object 2, course object ...., course object x],
# [enemy 1, enemy 2, enemy ..., enemy x]
# types:
# str, list of TerrainElements

game = Game()
