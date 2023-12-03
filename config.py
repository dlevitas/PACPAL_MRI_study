import os
import pygame

# experiment variables
data_dir = os.path.join(os.getcwd(), "data")
log_interval = 1  # sec (default is 0.5; ideally should reflect the scanner TR)
response_device = "mri"  # either "keyboard" or "mri" or "test"

run_length = 10  # min
start_run_buffer_time = 6  # sec
ITI_list = [3]  # sec (values used to create an exponential distribution of possible ITI times)
ITI_distribution_type = "exponential"  # either "exponential" or "normal"
end_run_buffer_time = 6  # sec

green_best_dir_level = 75  # integer ranging from 1-100. Probability of ghosts venturing towards dot
red_best_dir_level = 90  # integer ranging from 1-100. Probability of ghosts chasing player
ghost_color_len = 15  # sec
player_max_speed = 3  # (can be either 2 or 3)

health_bump = 25  # pixels
health_decay = 0.10  # px/sec. Decay rate of health bar, in pixels per second
bonus_increase = 0.05  # $$ (1.00 = $1, 0.50 = $0.50, etc)
loss_penalty = 0.10  # $$. How much money is lost when caught by ghosts or when health reaches 0
num_dots = 15  # how many dots there will be (in total) on each grid map

# pygame variables
keyboard_right_key = pygame.K_RIGHT
keyboard_left_key = pygame.K_LEFT
keyboard_up_key = pygame.K_UP
keyboard_down_key = pygame.K_DOWN

mri_right_key = pygame.K_r
mri_left_key = pygame.K_l
mri_up_key = pygame.K_u
mri_down_key = pygame.K_d
mri_capital_key = pygame.K_LSHIFT

test_right_key = pygame.K_i
test_left_key = pygame.K_j
test_up_key = pygame.K_e
test_down_key = pygame.K_f

practice_begin_key = pygame.K_RETURN
exp_begin_key = pygame.K_BACKQUOTE

# variables below are hard coded; adjusting them will break game
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 648

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
