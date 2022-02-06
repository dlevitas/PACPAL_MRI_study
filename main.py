from __future__ import division
import os
import pygame
import random
import numpy as np
import pandas as pd
from config import *
from game import Game
from layout import enviroment_setup, draw_enviroment
from exp import quit_check, Instructions, participant_info, save_data

# experiment variables:
data_dir = os.path.join(os.getcwd(), "data") # don't change
log_interval = 1 # sec (default is 1; don't change. Ideally should reflect the scanner TR)

run_length = 12 # min (default is 12)
start_run_buffer_time = 2 # sec (default is 8)
ITI_buffer_time = 2 # sec (default is 6)
end_run_buffer_time = 8 # sec (default is 8)

safe_chase_level = 0 # can be any integer ranging from 1-100 (default is 20)
threat_chase_level = 10  # can be any integer ranging from 1-100 (default is 80)
sal_period_len = 10 # sec (default is 15)
player_speed = 1 # (default is 1; value MUST be integer and not decimal)


def main():
    # Get participant info
    subID, runID = participant_info()

    # Set path(s) for saved data
    if not os.path.isdir("{}".format(data_dir)):
        os.mkdir("{}".format(data_dir))
    if not os.path.isdir("{}/sub-{}".format(data_dir, subID)):
        os.mkdir("{}/sub-{}".format(data_dir, subID))

    # Initialize all imported pygame modules
    pygame.init()

    # Set the width and height of the screen [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Set the current window caption
    pygame.display.set_caption("PACMAN")

    # clock
    clock = pygame.time.Clock()

    # Variables to loop over through experiment
    run_over = False
    pre_exp = True
    start_buffer = True
    end_buffer = True

    # salience period variables
    sal_period_info = {"safe": safe_chase_level, "threat": threat_chase_level}
    sal_period, slime_chase_level = random.choice(list(sal_period_info.items()))

    # Set timers and index values for experiment
    cum_run_time = 0
    logging_timer = 0
    sal_period_timer_index = 1
    logging_timer_index = 1

    # trial variables information
    trial = 1
    trial_info_list = []

    # Create game and instructions objects
    # game = Game(player_speed)
    grid, player_start_pos, slimes_start_pos, dot_locs, grid_id, horizontal, vertical, intersection_2way, intersection_3way, intersection_4way = enviroment_setup(trial)
    all_points_info = horizontal + vertical + intersection_2way + intersection_3way + intersection_4way
    game = Game(player_speed, grid, player_start_pos, slimes_start_pos, dot_locs, grid_id, horizontal, vertical, intersection_2way, intersection_3way, intersection_4way, all_points_info)

    instructions = Instructions("pre", 0, 0, 0, "N/A", run_length, end_run_buffer_time)

    # display waiting screen until scanner sends trigger signaling the beginning of the scan
    while pre_exp:
        pre_exp = instructions.process_events()
        instructions.display_frame(screen)

    # determine how much time elapsed from pygame initiation to right before start of run (i.e. now)
    pre_run_elapsed_time = pygame.time.get_ticks()

    # -------- Experiment Run Loop -----------
    while not run_over:
        clock.tick(60) # limit to 60 frames/sec

        cum_run_time = pygame.time.get_ticks() - pre_run_elapsed_time
        sal_period_timer = pygame.time.get_ticks() - pre_run_elapsed_time - start_run_buffer_time*1000
        logging_timer = pygame.time.get_ticks() - pre_run_elapsed_time - start_run_buffer_time*1000

        while start_buffer:
            instructions.__init__("start", start_run_buffer_time, pre_run_elapsed_time, 0, game.trial_end_reason, run_length, end_run_buffer_time)
            start_buffer = instructions.process_events()
            instructions.display_frame(screen)

        # --- Process events (keystrokes, mouse clicks, etc)
        run_over = game.process_events()
        # --- Game logic should go here
        trial_over = game.run_logic(trial, sal_period, slime_chase_level)
        # --- Draw the current frame
        game.display_frame(screen)

        # Log game information every log interval (1 sec), but not during ITI period
        if logging_timer/logging_timer_index >= log_interval*1000:
            logging_timer_index += 1

            if not trial_over:
                info = game.log_information()
                info["cum_run_time"] = cum_run_time/1000
                trial_info_list.append(info)

        if not trial_over:
            if sal_period_timer/sal_period_timer_index >= sal_period_len*1000:
                sal_period, slime_chase_level = [x for x in sal_period_info.items() if x[0] != sal_period][0]
                sal_period_timer_index += 1

        else: # inter trial interval (ITI) buffer period
            save_data(data_dir, subID, runID, trial, game, trial_info_list)
            trial_info_list = []
            trial += 1
            ITI_buffer = True
            run_elapsed_time = pygame.time.get_ticks()
            instructions.__init__("ITI", ITI_buffer_time, pre_run_elapsed_time, run_elapsed_time, game.trial_end_reason, run_length, end_run_buffer_time)

            while ITI_buffer:
                ITI_buffer = instructions.process_events()
                instructions.display_frame(screen)

            # change salience period if player lasted more than 3 sec (3000 ms)
            # print(sal_period_timer/sal_period_timer_index)
            if sal_period_timer/sal_period_timer_index > 3000 + ITI_buffer_time*1000:
                # print('cool')
                sal_period, slime_chase_level = [x for x in sal_period_info.items() if x[0] != sal_period][0]
                sal_period_timer_index += 1

        # Stop presentation several seconds before the end of the run, based on the end_run_buffer_time variable value
        if cum_run_time >= run_length*60*1000 - end_run_buffer_time*1000:
            run_elapsed_time = pygame.time.get_ticks()
            instructions.__init__("end", end_run_buffer_time, pre_run_elapsed_time, run_elapsed_time, game.trial_end_reason, run_length, end_run_buffer_time)

            while end_buffer:
                end_buffer = instructions.process_events()
                instructions.display_frame(screen)
            run_over = True

    """ Run over, save data if it wasn't already. This would occur if we quit
    before the current trial was over.
    """
    if len(trial_info_list):
        save_data(data_dir, subID, runID, trial, game, trial_info_list)

    # Quit the game
    pygame.quit()

if __name__ == '__main__':
    main()
