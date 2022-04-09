import os
import pygame

# experiment variables
data_dir = os.path.join(os.getcwd(), "data")
log_interval = 1 # sec (default is 0.5; ideally should reflect the scanner TR)
response_device = "test" # either "keyboard" or "mri" or "test"

run_length = 10 # min
start_run_buffer_time = 6 # sec
ITI_buffer_times = [3,4,5] # sec (values used to create an exponential distribution of possible ITI times)
end_run_buffer_time = 6 # sec

safe_chase_level = 10 # an integer ranging from 1-100
threat_chase_level = 90  # an integer ranging from 1-100
sal_period_len = 15 # sec
player_max_speed = 3 # (can be either 2 or 3)

health_bump = 20 # pixels
health_decay = 0.10 # px/sec. Decay rate of health bar, in pixels per second
bonus_increase = 0.06 # in cents ($1 = 1.00, 50 cents = 0.50, etc)
loss_penalty = 0.02 # $$. How much money is lost when caught by ghosts or when health reaches 0


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

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 648

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
