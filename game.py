import pygame
from config import *
from player import Player
from scipy.spatial import distance
from ghosts import Block, Ellipse, ghost
from layout import enviroment_setup, draw_enviroment

class Game(object):
    def __init__(self, player_max_speed, grid, player_start_pos, ghosts_start_pos, 
                 dots_info, grid_id, horizontal, vertical, intersection_2way, 
                 intersection_3way, intersection_4way, all_points_info, cum_bonus, 
                 sal_period, loss_penalty, health_decay, ghosts_threat_speed_options,
                 health_bump, bonus_increase):

        self.run_over = True
        self.trial_over = True
        self.bonus_increase = bonus_increase
        self.cum_bonus = cum_bonus
        self.dots_info = dots_info # location of dots on grid
        self.font = pygame.font.Font(None, 30) # font for displaying the cumulative bonus on the screen
        self.trial_end_reason = "N/A" # caught, no_health, or won
        self.player_max_speed = player_max_speed # fastest speed player can go
        self.sal_period = sal_period
        self.health_decay = health_decay

        # Create the player
        self.player = Player(player_start_pos[0], player_start_pos[1], "player.png", self.player_max_speed, self.health_decay)
        self.player.start_pos = player_start_pos
        
        # Create the blocks that will set the paths where the player can go
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        self.intersection_blocks = pygame.sprite.Group()
        
        # Create a group for the dots on the screen
        self.dots_collected = 0
        self.dots_info = dots_info
        self.dots_group = pygame.sprite.Group()
        # Add the dots inside the game
        for dot_info in dots_info:
            if dot_info[1] == min([x[1] for x in self.dots_info]):
                self.visible_dot_loc = dot_info[0]
                self.dots_group.add(Ellipse(dot_info[0][0]+10, dot_info[0][1]+10, WHITE, 15, 15))

        # specify direction player is moving
        self.player.direction_facing = "still"

        # specify which grid is being used for this trial
        self.grid_id = grid_id

        # set the enviroment
        self.grid = grid
        
        # set player health level
        self.health = 100
        self.health_bump = health_bump

        self.all_points_info = all_points_info
        
        self.ghosts_threat_speed_options = ghosts_threat_speed_options

        for h in horizontal:
            self.horizontal_blocks.add(Block(h[0][0]+8, h[0][1]+8, RED, 16, 16))
        for v in vertical:
            self.vertical_blocks.add(Block(v[0][0]+8, v[0][1]+8, RED, 16, 16))
        for i in intersection_2way + intersection_3way + intersection_4way:
            self.intersection_blocks.add(Block(i[0][0]+8, i[0][1]+8, GREEN, 16, 16))

        # Create the ghosts
        self.ghosts = pygame.sprite.Group()
        self.ghosts.add(ghost(ghosts_start_pos[0][0], ghosts_start_pos[0][1], 0, self.player_max_speed, self.ghosts_threat_speed_options))
        self.ghosts.add(ghost(ghosts_start_pos[1][0], ghosts_start_pos[1][1], 0, -self.player_max_speed, self.ghosts_threat_speed_options))
        self.ghosts.start_pos = ghosts_start_pos


    def keyboard_process_events(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # exit program entirely
                    self.run_over = True
                    return True
                elif event.key == keyboard_right_key:
                    self.player.move_right()
                    self.player.direction_facing = "right"

                elif event.key == keyboard_left_key:
                    self.player.move_left()
                    self.player.direction_facing = "left"

                elif event.key == keyboard_up_key:
                    self.player.move_up()
                    self.player.direction_facing = "up"

                elif event.key == keyboard_down_key:
                    self.player.move_down()
                    self.player.direction_facing = "down"

            elif event.type == pygame.KEYUP:
                if event.key == keyboard_right_key:
                    self.player.stop_move_right()
                elif event.key == keyboard_left_key:
                    self.player.stop_move_left()
                elif event.key == keyboard_up_key:
                    self.player.stop_move_up()
                elif event.key == keyboard_down_key:
                    self.player.stop_move_down()
        return False
    
    def test_process_events(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # exit program entirely
                    self.run_over = True
                    return True
                elif event.key == test_right_key:
                    self.player.move_right()
                    self.player.direction_facing = "right"

                elif event.key == test_left_key:
                    self.player.move_left()
                    self.player.direction_facing = "left"

                elif event.key == test_up_key:
                    self.player.move_up()
                    self.player.direction_facing = "up"

                elif event.key == test_down_key:
                    self.player.move_down()
                    self.player.direction_facing = "down"

            elif event.type == pygame.KEYUP:
                if event.key == test_right_key:
                    self.player.stop_move_right()
                elif event.key == test_left_key:
                    self.player.stop_move_left()
                elif event.key == test_up_key:
                    self.player.stop_move_up()
                elif event.key == test_down_key:
                    self.player.stop_move_down()
        return False    
            
            
    def mri_process_events(self):
        counter = []
        for event in pygame.event.get(): # User did something
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # exit program entirely
                    self.run_over = True
                    return True
                else: # direction movement
                    if event.key in [mri_capital_key, mri_right_key, mri_left_key, mri_up_key, mri_down_key]:
                        counter.append(pygame.key.name(event.key))
                    # right
                    if len(counter) == 2 and counter[0] == "left shift" and counter[1] == "r":
                        self.player.move_right()
                        self.player.direction_facing = "right"
                    elif len(counter) == 1 and counter[0] == "r":
                        self.player.stop_move_right()
                    # left
                    if len(counter) == 2 and counter[0] == "left shift" and counter[1] == "l":
                        self.player.move_left()
                        self.player.direction_facing = "left"
                    elif len(counter) == 1 and counter[0] == "l":
                        self.player.stop_move_left()
                    # up
                    if len(counter) == 2 and counter[0] == "left shift" and counter[1] == "u":
                        self.player.move_up()
                        self.player.direction_facing = "up"
                    elif len(counter) == 1 and counter[0] == "u":
                        self.player.stop_move_up()
                    # down
                    if len(counter) == 2 and counter[0] == "left shift" and counter[1] == "d":
                        self.player.move_down()
                        self.player.direction_facing = "down"
                    elif len(counter) == 1 and counter[0] == "d":
                        self.player.stop_move_down()
        return False              
            
            
    def run_logic(self, rand_num, sal_period, ghost_best_dir_level):
        self.sal_period = sal_period
        self.ghost_best_dir_level = ghost_best_dir_level

        if self.trial_over:
            grid, player_start_pos, ghosts_start_pos, dots_info, grid_id, horizontal, vertical, intersection_2way, intersection_3way, intersection_4way = enviroment_setup(rand_num, num_dots)
            all_points_info = horizontal + vertical + intersection_2way + intersection_3way + intersection_4way
            self.__init__(self.player_max_speed, grid, player_start_pos, 
                          ghosts_start_pos, dots_info, grid_id, horizontal, 
                          vertical, intersection_2way, intersection_3way, 
                          intersection_4way, all_points_info, self.cum_bonus, 
                          self.sal_period, loss_penalty, self.health_decay, 
                          self.ghosts_threat_speed_options, self.health_bump,
                          self.bonus_increase)
            self.run_over = False
            self.trial_over = False

        else:
            self.player.update(self.horizontal_blocks, self.vertical_blocks, self.intersection_blocks, self.all_points_info)
            # When the block_hit_list contains one sprite that means that player hit a dot
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            if len(block_hit_list) > 0:
                eaten_dot_loc = min([x[0] for x in self.dots_info], key=lambda c: (c[0] - self.player.rect.topleft[0])**2 + (c[1] - self.player.rect.topleft[1])**2)
                eaten_dot_index = [x[1] for x in self.dots_info if eaten_dot_loc in x][0]
                if eaten_dot_index == min([x[1] for x in self.dots_info]):
                    self.dots_info = [x for x in self.dots_info if eaten_dot_loc not in x]
                    self.cum_bonus += self.bonus_increase
                    self.player.health += self.health_bump
                    self.dots_collected += 1

            block_hit_list = pygame.sprite.spritecollide(self.player, self.ghosts, True)
            if len(block_hit_list) > 0: # caught by ghost
                self.player.explosion = True
                self.trial_over = True
                self.trial_end_reason = "caught"
                return True

            elif self.player.health <= 0: # health bar reached 0
                self.trial_over = True
                self.trial_end_reason = "no_health"
                return True

            elif len(self.dots_info) == 0: # consumed all dots
                self.trial_over = True
                self.trial_end_reason = "won"
                return True
            
            self.trial_over = self.player.trial_over
            self.ghosts.update(self.horizontal_blocks, self.vertical_blocks, self.intersection_blocks, self.player.rect.topleft, self.visible_dot_loc, self.all_points_info, self.sal_period, self.ghost_best_dir_level)
            
            self.dots_group.add(Ellipse(self.dots_info[0][0][0]+10, self.dots_info[0][0][1]+10, WHITE, 15, 15))
            self.visible_dot_loc = self.dots_info[0][0]

        return False

    def display_frame(self, screen):
        screen.fill(BLACK)

        # draw the game here
        draw_enviroment(screen, self.grid)
        self.dots_group.draw(screen)
        self.ghosts.draw(screen)
        screen.blit(self.player.image, self.player.rect)
        # Render the text for the cumulative bonus
        bonus_text = self.font.render("total bonus: $" + str(round(self.cum_bonus,2)), True, GREEN)
        dot_text = self.font.render("dots collected: {}/15".format(str(self.dots_collected)), True, WHITE)
        # Put the text on the screen
        screen.blit(bonus_text, [80, 0])
        screen.blit(dot_text, [600, 0])

        # display health bar
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH/2.5, 5, 100, 15))
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH/2.5, 5, self.player.health, 15))

        # update the screen with what has been drawn.
        pygame.display.flip()

    def log_information(self):
        info = {}
        ghost_locations = []
        ghost_distances_from_player_manhattan = []
        ghost_distances_from_player_euclidean = []
        dot_distances_from_player_manhattan = []
        dot_distances_from_player_euclidean = []
        info["grid_ID"] = self.grid_id
        info["player_start_pos"] = self.player.start_pos
        info["ghosts_start_pos"] = self.ghosts.start_pos
        info["player_loc"] = self.player.rect.topleft
        info["player_max_speed"] = self.player_max_speed
        
        # if you "lose" trial, incur penalty
        if self.trial_end_reason in ["caught", "no_health"]:
            self.cum_bonus -= loss_penalty
        if self.cum_bonus < 0: # if negative bonus value, set to 0
            self.cum_bonus = 0.00
            
        for g in self.ghosts.sprites():
            ghost_locations.append(g.rect.topleft)
            
            ghost_dist_from_player_manhattan = distance.cityblock(list(self.player.rect.topleft), list(g.rect.topleft))
            ghost_dist_from_player_manhattan = int(round(ghost_dist_from_player_manhattan, 0))
            ghost_distances_from_player_manhattan.append(ghost_dist_from_player_manhattan)
            
            ghost_dist_from_player_euclidean = distance.euclidean(list(self.player.rect.topleft), list(g.rect.topleft))
            ghost_dist_from_player_euclidean = int(round(ghost_dist_from_player_euclidean, 0))
            ghost_distances_from_player_euclidean.append(ghost_dist_from_player_euclidean)
            

        for dot_loc in self.dots_info:
            dot_dist_from_player_manhattan = distance.cityblock(list(self.player.rect.topleft),list(dot_loc[0]))
            dot_dist_from_player_manhattan = int(round(dot_dist_from_player_manhattan, 0))
            dot_distances_from_player_manhattan.append(dot_dist_from_player_manhattan)
            
            dot_dist_from_player_euclidean = distance.euclidean(list(self.player.rect.topleft),list(dot_loc[0]))
            dot_dist_from_player_euclidean = int(round(dot_dist_from_player_euclidean, 0))
            dot_distances_from_player_euclidean.append(dot_dist_from_player_euclidean)

        
        if self.trial_end_reason == "caught":
            self.closest_ghost_dist_manhattan = 0
            self.closest_ghost_dist_euclidean = 0
        else:
            if len(ghost_distances_from_player_manhattan) == 2:
                self.closest_ghost_dist_manhattan = min(ghost_distances_from_player_manhattan)
                self.closest_ghost_dist_euclidean = min(ghost_distances_from_player_euclidean)
            else:
                self.closest_ghost_dist_manhattan = 0
                self.closest_ghost_dist_euclidean = 0
                
            
        if self.trial_end_reason == "won":
            self.visible_dot_dist_manhattan = 0
            self.visible_dot_dist_euclidean = 0
        else:
            if len(dot_distances_from_player_manhattan):
                self.visible_dot_dist_manhattan = min(dot_distances_from_player_manhattan)
                self.visible_dot_dist_euclidean = min(dot_distances_from_player_euclidean)
            else:
                self.visible_dot_dist_manhattan = 0
                self.visible_dot_dist_euclidean = 0


        info["ghosts_locs"] = ghost_locations
        info["all_dots_locs"] = [x[0] for x in self.dots_info]
        info["visible_dot_loc"] = self.visible_dot_loc
        info["ghosts_dists_from_player_manhattan"] = ghost_distances_from_player_manhattan
        info["ghosts_dists_from_player_euclidean"] = ghost_distances_from_player_euclidean
        info["visible_dot_dist_from_player_manhattan"] = self.visible_dot_dist_manhattan
        info["visible_dot_dist_from_player_euclidean"] = self.visible_dot_dist_euclidean
        info["closest_ghost_dist_manhattan"] = self.closest_ghost_dist_manhattan
        info["closest_ghost_dist_euclidean"] = self.closest_ghost_dist_euclidean
        info["salience_period"] = self.sal_period
        try:
            info["ghosts_best_dir_level"] = self.ghosts.sprites()[0].best_dir_level
            info["ghosts_speed"] = self.ghosts.sprites()[0].speed
        except:
            info["ghosts_best_dir_level"] = 10
            info["ghosts_speed"] = self.player_max_speed
        info["player_direction_facing"] = self.player.direction_facing
        info["cumulative_bonus"] = round(self.cum_bonus,2)
        info["health"] = round(self.player.health, 2)
        info["trial_end_reason"] = self.trial_end_reason

        return info