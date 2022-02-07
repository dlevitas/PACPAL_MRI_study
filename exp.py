from __future__ import division
import os
import game
import pygame
import pandas as pd
from config import *


def quit_check():
    """Quit game is escape key is pressed."""
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()


class Instructions(object):
    """Display instructions during different parts of game."""
    
    def __init__(self, period, buffer_time, pre_run_elapsed_time, run_elapsed_time, trial_end_reason, run_length, end_buffer_time):
        self.text = "Please wait for the scan to begin"
        self.font_color = WHITE
        self.select_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 30)
        self.period = period
        self.buffer_time = buffer_time
        self.pre_run_elapsed_time = pre_run_elapsed_time
        self.run_elapsed_time = run_elapsed_time
        self.trial_end_reason = trial_end_reason
        self.run_length = run_length
        self.end_buffer_time = end_buffer_time

    def process_events(self):
        if self.period != "pre":
            quit_check()

        if self.period == "start":
            self.cum_run_time = pygame.time.get_ticks() - self.pre_run_elapsed_time
        elif self.period == "ITI":
            self.cum_run_time = pygame.time.get_ticks() - self.run_elapsed_time
        else:
            self.cum_run_time = pygame.time.get_ticks() - self.run_elapsed_time

        self.countdown = (self.buffer_time*1000 - self.cum_run_time)/10

        if self.period == "pre":
            self.text = "Please wait for the experiment to begin"
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    elif event.key == pygame.K_BACKQUOTE:
                        return False

        elif self.period == "start":
            self.text = "Please wait. The run will begin shortly"
            if self.cum_run_time >= self.buffer_time*1000:
                return False

        elif self.period == "ITI":
            if self.trial_end_reason in ["killed", "starved"]:
                self.text = "You lost. Please wait several seconds for the next trial to begin"
            else:
                self.text = "You won. Please wait several seconds for the next trial to begin"

            # quit out if ITI buffer period runs into end run buffer period
            if pygame.time.get_ticks() >= self.run_elapsed_time + self.end_buffer_time*1000:
                return False
            if pygame.time.get_ticks() >= self.run_elapsed_time + self.buffer_time*1000:
                return False

        elif self.period == "end":
            self.text = "This run will end in several seconds"
            if self.cum_run_time >= self.end_buffer_time*1000:
                return False

        return True


    def display_frame(self, screen):
        screen.fill(BLACK)

        label = self.font.render(self.text, True, self.select_color)

        width = label.get_width()
        height = label.get_height()

        posX = (SCREEN_WIDTH/2) - (width/2)
        posY = (SCREEN_HEIGHT/2) - (label.get_height()/2)

        if self.period != "pre":
            pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH/2.5, SCREEN_HEIGHT/1.8, self.countdown/2, 15))

        screen.blit(label, (posX, posY))

        pygame.display.flip()


def participant_info():
    """Allows experimenter to enter participant ID and run ID and checks to 
    ensure that they are proper (e.g. no non-alphanumeric characters allowed)."""
    
    print("Enter subject ID:")
    s = input()

    print("Enter run ID:")
    r = input()

    print("------------------")

    subID = s
    runID = r

    if not subID.isalnum():
        raise ValueError("The subID contains non-alphanumeric character(s). Please restart.")

    try:
        if not int(runID):
            raise ValueError("The runID is not an integer value. Please restart.")
    except:
        raise ValueError("The runID is not an integer value. Please restart.")

    return subID, runID


def save_data(data_dir, subID, runID, trial, game, trial_info_list):
    """Saves data to TSV file. A file is generated for each trial of each run
    of each subject."""
    
    if not os.path.isfile("{}/sub-{}/run-{}_trial-{}.tsv".format(data_dir, subID, runID, trial)):
        df = pd.DataFrame(trial_info_list)
        df.to_csv("{}/sub-{}/run-{}_trial-{}.tsv".format(data_dir, subID, runID, trial),
                  sep="\t", index=False, columns=list(game.log_information().keys()))


