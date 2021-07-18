# Hero of Aeboria settings file
# includes all relevant settings variables, including window size, terrain blocks, gravity, and frame-rate

target_frame_rate = 60
window_x_size = 1366
window_y_size = 768

# thanks to modifications, the x_coordinate is now matched to the left side, and not at the midpoint, which
# was intensely confusing. Infrastructure has been put in place to match the y coordinate to the top, but the
# default (with y at bottom) has been left to play nicely with window_y_height if needed. Drawback of this system
# is that the y coordinate displayed in the collision system does not match definitions made here.

# screen resolution has been switched to 1366 x 768, the maximum HD ratio size this computer will
# support during development. Terrain blocks are being defined statically at this ratio. If support
# for varying screen sizes is added at a later stage, scaling math with have to be done on these blocks
# based on this development resolution

# terrain block format is x coord, y coord, width, height

terrain_list = [(-1000, 768, 1900, 100),    # starting ground
                (-500, 768, 50, 1366),      # (to be made invisible) left wall
                (900, 768, 75, 550),        # cliff start/left wall
                (975, 268, 300, 50),        # cliff roof
                (940, 218, 270, 65),        # cliff cap
                (870, 568, 30, 30),         # cliff low rung
                (670, 468, 50, 30),         # cliff middle rung
                (870, 368, 30, 30),         # cliff top rung
                # end of first part of starting area, start of part two
                (1325, 538, 95, 320),       # cliff right edge
                (1420, 480, 27, 140),       # cliff right edge jagged bottom
                (1420, 315, 45, 85),        # cliff right edge jagged top
                (1465, 425, 22, 60),        # cliff right edge floating first
                (1545, 415, 42, 27),        # cliff right edge floating second
                (1505, 290, 17, 45),        # cliff right edge floating third
                (1025, 380, 300, 30),       # cliff top internal
                (975, 520, 250, 30),        # cliff middle internal
                (975, 768, 550, 155),       # cliff bottom
                (1525, 750, 80, 38),        # lower cliff jagged right edge bottom
                (1525, 705, 125, 67),       # lower cliff jagged right edge top
                (1685, 680, 60, 35),        # lower cliff floating first
                (1675, 745, 30, 50),        # lower cliff floating second
                (1790, 675, 45, 25),        # lower cliff floating third
                (1950, 575, 150, 35),       # first floating platform
                # end of starting area
                (2100, 450, 210, 30),       # 1st second stage platform, stage start x is 2100
                (2350, 330, 90, 40),        # 2nd platform, middle
                (2510, 280, 40, 30),        # rock after 2nd platform
                (2480, 390, 25, 30),        # lower rock after 2nd platform for back-track
                (2540, 515, 290, 35),       # 3rd range, lower, 2500 - 2600
                (2610, 310, 200, 35),       # 3rd range, upper
                (2800, 630, 200, 40),       # 4th range, lower, 2800 - 3000
                (2950, 250, 170, 35),       # 4th range, upper
                (3020, 730, 310, 50),       # 5th range, lower (heart here?), 3000 - 3200
                (3200, 190, 150, 35),       # 5th range, upper
                (3100, 490, 200, 40),       # 5th range, middle
                (3170, 350, 40, 30),        # 5th range, upper middle rock
                (3600, 730, 180, 35),       # 6th range, lower, 3400 - 3700
                (3700, 600, 40, 40),        # 6th range, lower rock
                (3450, 510, 120, 30),       # 6th range, upper middle
                (3500, 80, 50, 30),         # 6th range, upper
                (3660, 230, 120, 35),       # 6th range, upper second
                (3850, 380, 130, 45),       # 7th range, middle out, 3800 - 4000
                (3900, 700, 80, 35),       # 7th range, lower out
                (3870, 150, 110, 50),       # 7th range, upper out
                ]

# General stage drafting notes:
# Each stage should be 2000 pixels long in the x direction and have a mix of terrain
# features, hearts, and enemies. Critically, each stage needs to have a common in and out
# compatibility, at the least having an accessible ending platform around screen middle
# (x = 384, ~= 380) and a starting terrain feature which is accessible either by fall or jump from
# the previous stage's terrain feature at x ~= 380.
# Doing this is a bit reductive in terms of stage design, but allows for the possibility of random
# stage assignment: as long as stages are compatible with each other, then theoretically they could
# be presented in any order (after the two starting stages).


gravity = 0.35
friction_constant = -0.07
side_scroll_speed = 1
hero_start_position_x, hero_start_position_y = 1050, 50

old_terrain_list = [(-2000, 400, 5000, 20), (300, 350, 100, 50), (500, 325, 100, 50), (700, 300, 100, 50),
                    (900, 300, 200, 50), (1100, 300, 50, 500), (-200, 310, 350, 50), (-210, 315, 100, 75),
                    (-190, 350, 30, 50), (2500, 400, 50, 50)]

