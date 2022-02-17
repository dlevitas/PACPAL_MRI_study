from __future__ import division
import os
import glob
import pygame
import random
import pandas as pd
from config import *
from game import Game
from layout import enviroment_setup
from exp import Instructions, participant_info, save_data, gauss_choice

# experiment variables. Can be modified but should remain constant once data collection for study begins:
data_dir = os.path.join(os.getcwd(), "data") # don't change
log_interval = 1 # sec (default is 1; don't change. Ideally should reflect the scanner TR)

run_length = 12 # min (default is 12)
start_run_buffer_time = 8 # sec (default is 8)
#ITI_buffer_time = 8 # sec (default is 8)
ITI_buffer_times = [6,7,8,9,10] # sec (will randomly select ITI buffer time in gaussian distribution fashion (i.e. 8 most common)
end_run_buffer_time = 8 # sec (default is 8)

safe_chase_level = 20 # an integer ranging from 1-100 (default is 0)
threat_chase_level = 80  # an integer ranging from 1-100 (default is 100)
sal_period_len = 15 # sec (default is 15)
player_speed = 3 # (default is 3; can be either 2 or 3)

# Begin
def main():
    """Runs the PACMAN game. All classes and functions are referenced here."""
    
    # get participant info
    subID, runID = participant_info()

    # set path(s) for saved data
    if not os.path.isdir("{}".format(data_dir)):
        os.mkdir("{}".format(data_dir))
    if not os.path.isdir("{}/sub-{}".format(data_dir, subID)):
        os.mkdir("{}/sub-{}".format(data_dir, subID))
    if len([x for x in os.listdir("{}/sub-{}".format(data_dir, subID)) if "run-{}".format(runID) in x]):
        raise ValueError("There is already data saved for run {}. Please select the next run number.".format(runID))

    # initialize all imported pygame modules
    pygame.init()

    # set the width and height of the screen [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # set the current window caption
    pygame.display.set_caption("PACMAN")

    # clock
    clock = pygame.time.Clock()
    
    # set timers and index values for experiment
    cum_run_time = 0
    logging_timer = 0
    sal_period_timer_index = 1
    logging_timer_index = 1
    ITI_index = 0
    cum_ITI_buffer_time = 0

    # variables to loop over through experiment
    run_over = False
    pre_exp = True
    start_buffer = True
    end_buffer = True

    # salience period variables
    sal_period_info = {"safe": safe_chase_level, "threat": threat_chase_level}
    sal_period, ghost_chase_level = random.choice(list(sal_period_info.items()))

    # trial variables information
    trial = 1
    trial_info_list = []
    ITI_buffer_time = random.choice(ITI_buffer_times)
    rand_num = random.randrange(100) # used to set seed that randomizes grid and player/ghosts locations
    
    # determine cumulative experiment bonus amount and trial number
    try:
        recent_log_file = sorted([x for x in glob.glob("{}/data/sub-{}/*.tsv".format(os.getcwd(), subID)) if "run-0" not in x])[-1]
        trial = int(recent_log_file.split("trial-")[1].split(".tsv")[0])
        bonus = pd.read_csv(recent_log_file, sep="\t")["bonus"].iloc[-1]
    except:
        trial = 1
        bonus = 0.00
        

    # create game and instructions objects
    grid, player_start_pos, ghosts_start_pos, dot_locs, grid_id, horizontal, vertical, intersection_2way, intersection_3way, intersection_4way = enviroment_setup(rand_num)
    all_points_info = horizontal + vertical + intersection_2way + intersection_3way + intersection_4way
    game = Game(player_speed, grid, player_start_pos, ghosts_start_pos, dot_locs, grid_id, horizontal, vertical, intersection_2way, intersection_3way, intersection_4way, all_points_info, bonus, sal_period, loss_penalty)
    instructions = Instructions("pre", 0, 0, 0, "N/A", run_length, end_run_buffer_time, runID)

    # display waiting screen until scanner sends trigger signaling the beginning of the scan
    while pre_exp:
        pre_exp = instructions.process_events()
        instructions.display_frame(screen)

    # determine how much time elapsed from pygame initiation to right before start of run (i.e. now)
    pre_run_elapsed_time = pygame.time.get_ticks()

    # -------- Experiment run loop -----------
    while not run_over:
        clock.tick(30) # limit to 30 frames/sec

        cum_run_time = pygame.time.get_ticks() - pre_run_elapsed_time

        while start_buffer:
            instructions.__init__("start", start_run_buffer_time, pre_run_elapsed_time, 0, game.trial_end_reason, run_length, end_run_buffer_time, runID)
            start_buffer = instructions.process_events()
            instructions.display_frame(screen)

        # process events (keystrokes, mouse clicks, etc) and check if run ends
        run_over = game.process_events()
        # game logic is here, including checking for when the trial ends
        trial_over = game.run_logic(rand_num, sal_period, ghost_chase_level)
        # draw the current frame
        game.display_frame(screen)
        
        if not trial_over:
#            if not len(trial_info_list): # let first row of log be the trial onset information
#                info = game.log_information()
#                info["cum_run_time"] = (pygame.time.get_ticks() - pre_run_elapsed_time)/1000
#                info["round_cum_run_time"] = round(info["cum_run_time"])
#                info["ITI_length"] = ITI_buffer_time
#                trial_info_list.append(info)
            
            logging_timer = pygame.time.get_ticks() - pre_run_elapsed_time - start_run_buffer_time*1000 - cum_ITI_buffer_time*1000
            sal_period_timer = pygame.time.get_ticks() - pre_run_elapsed_time - start_run_buffer_time*1000 - cum_ITI_buffer_time*1000              

            # log game information every log interval, but not in-between trials
            if logging_timer/logging_timer_index >= log_interval*1000:
                logging_timer_index += 1
    
                info = game.log_information()
                info["cum_run_time"] = cum_run_time/1000
                info["round_cum_run_time"] = round(info["cum_run_time"])
                info["ITI_length"] = ITI_buffer_time
                trial_info_list.append(info)

            # update salience period
            if sal_period_timer/sal_period_timer_index >= sal_period_len*1000:
                sal_period, ghost_chase_level = [x for x in sal_period_info.items() if x[0] != sal_period][0]
                sal_period_timer_index += 1

        else: # trial ends, enter inter trial interval (ITI) buffer period
            if len(trial_info_list): # add log information from trial offset, even if not at log interval
                info = game.log_information()
                info["cum_run_time"] = cum_run_time/1000
                info["round_cum_run_time"] = round(info["cum_run_time"])
                info["ITI_length"] = ITI_buffer_time
                trial_info_list.append(info)
            
            save_data(data_dir, subID, runID, trial, trial_info_list)
            trial_info_list = []
            trial += 1
            ITI_index += 1
            rand_num = random.randrange(100)
            ITI_buffer = True
            run_elapsed_time = pygame.time.get_ticks()
            instructions.__init__("ITI", ITI_buffer_time, pre_run_elapsed_time, run_elapsed_time, game.trial_end_reason, run_length, end_run_buffer_time, runID)

            while ITI_buffer:
                ITI_buffer = instructions.process_events()
                instructions.display_frame(screen)
            
            cum_ITI_buffer_time += ITI_buffer_time
            ITI_buffer_time = gauss_choice(ITI_buffer_times)

        # stop game several seconds before the end of the run
        if cum_run_time >= run_length*60*1000 - end_run_buffer_time*1000:
            if len(trial_info_list): # add log information at trial offset, even if not at log interval
                info = game.log_information()
                info["cum_run_time"] = cum_run_time/1000
                info["round_cum_run_time"] = round(info["cum_run_time"])
                info["ITI_length"] = ITI_buffer_time
                info["trial_end_reason"] = "run_end"
                trial_info_list.append(info)
                
            run_elapsed_time = pygame.time.get_ticks()
            instructions.__init__("end", end_run_buffer_time, pre_run_elapsed_time, run_elapsed_time, game.trial_end_reason, run_length, end_run_buffer_time, runID)

            while end_buffer:
                end_buffer = instructions.process_events()
                instructions.display_frame(screen)
            run_over = True

    # save data if it wasn't already. Occurs if game quit before the current trial was over
    if len(trial_info_list):
        save_data(data_dir, subID, runID, trial, trial_info_list)

    # quit the game (i.e. end of run)
    pygame.quit()

if __name__ == '__main__':
    main()
