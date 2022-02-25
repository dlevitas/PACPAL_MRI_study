import os
import pygame

data_dir = os.path.join(os.getcwd(), "data") # location of log files
log_interval = 1 # sec. Ideally should reflect the scanner TR

run_length = 12 # min (default is 12)
start_run_buffer_time = 8 # sec (default is 8)
ITI_buffer_times = [6,7,8,9,10] # sec (will randomly select ITI buffer time in gaussian distribution fashion (i.e. 8 most common)
end_run_buffer_time = 8 # sec (default is 8)

safe_chase_level = 10 # an integer ranging from 1-100 (default is 0)
threat_chase_level = 90  # an integer ranging from 1-100 (default is 100)
sal_period_len = 15 # sec (default is 15)
player_speed = 3 # (default is 3; can be either 2 or 3)

health_decay = 0.2 # decay of health

right_key = pygame.K_i
left_key = pygame.K_j
up_key = pygame.K_e
down_key = pygame.K_f

loss_penalty = 0.03 # how much money ($) is lost after losing each trial

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 648

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
