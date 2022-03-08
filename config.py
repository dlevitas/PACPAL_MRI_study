import os
import pygame

#right_key = pygame.K_i
#left_key = pygame.K_j
#up_key = pygame.K_e
#down_key = pygame.K_f

# experiment variables
data_dir = os.path.join(os.getcwd(), "data")
log_interval = 0.5 # sec (default is 0.5; ideally should reflect the scanner TR)
response_device = "mri" # either "keyboard" or "mri"

run_length = 12 # min
start_run_buffer_time = 6 # sec
ITI_buffer_times = [2,3,4,5,6] # sec (will randomly select ITI buffer time in gaussian distribution fashion
end_run_buffer_time = 6 # sec

safe_chase_level = 10 # an integer ranging from 1-100 (default is 10)
threat_chase_level = 90  # an integer ranging from 1-100 (default is 90)
sal_period_len = 15 # sec
player_speed = 3 # (can be either 2 or 3)


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

practice_begin_key = pygame.K_RETURN
exp_begin_key = pygame.K_BACKQUOTE

loss_penalty = 0.03

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 648

health_decay = 0.20

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
