# hero of aeboria settings file
# all relevant setting variables, including window size, terrain blocks, gravity, and frame-rate

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
                (975, 268, 300, 50),        # cliff top
                (870, 568, 30, 30),         # cliff low rung
                (670, 468, 50, 30),         # cliff middle rung
                (870, 368, 30, 30),         # cliff top rung
                ]

gravity = 0.35
friction_constant = -0.07
side_scroll_speed = 1

old_terrain_list = [(500, 400, 5000, 20), (300, 350, 100, 50), (500, 325, 100, 50), (700, 300, 100, 50),
                    (900, 300, 200, 50), (1100, 300, 50, 500), (-200, 310, 350, 50), (-210, 315, 100, 75),
                    (-260, 350, 30, 50), (2500, 400, 50, 50)]
