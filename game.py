import pygame
from config import *
from player import Player
from scipy.spatial import distance
from ghosts import Block, Ellipse, ghost
from layout import enviroment_setup, draw_enviroment

class Game(object):
    def __init__(self, player_speed, grid, player_start_pos, ghosts_start_pos, dot_locs, grid_id, horizontal, vertical, intersection_2way, intersection_3way, intersection_4way, all_points_info):

        self.font = pygame.font.Font(None, 40)
        self.run_over = True
        self.trial_over = True
        self.score = 0
        self.dot_locs = dot_locs # location of dots on grid
        self.font = pygame.font.Font(None, 35) # font for displaying the score on the screen
        self.trial_end_reason = "killed" # killed, starved, or won
        self.player_speed = player_speed # how fast player can move

        # Create the player
        self.player = Player(player_start_pos[0], player_start_pos[1], "player.png", self.player_speed)
        self.player.start_pos = player_start_pos
        # Create the blocks that will set the paths where the player can go
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        self.intersection_blocks = pygame.sprite.Group()
        # Create a group for the dots on the screen
        self.dots_group = pygame.sprite.Group()

        # specify direction player is moving
        self.player.direction_moving = "still"

        # specify which grid is being used for this trial
        self.grid_id = grid_id

        # Set the enviroment:
        self.grid = grid

        self.all_points_info = all_points_info

        for h in horizontal:
            self.horizontal_blocks.add(Block(h[0][0]+8, h[0][1]+8, RED, 16, 16))
        for v in vertical:
            self.vertical_blocks.add(Block(v[0][0]+8, v[0][1]+8, RED, 16, 16))
        for i in intersection_2way + intersection_3way + intersection_4way:
            self.intersection_blocks.add(Block(i[0][0]+8, i[0][1]+8, GREEN, 16, 16))

        # Create the ghosts
        self.ghosts = pygame.sprite.Group()
        self.ghosts.add(ghost(ghosts_start_pos[0][0], ghosts_start_pos[0][1], 0, self.player_speed, self.player_speed))
        self.ghosts.add(ghost(ghosts_start_pos[1][0], ghosts_start_pos[1][1], 0, -self.player_speed, self.player_speed))

        # Add the dots inside the game
        for d in dot_locs:
            self.dots_group.add(Ellipse(d[0]+10, d[1]+10, WHITE, 15, 15))


    def process_events(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # exit program entirely
                    self.run_over = True
                    return True

                elif event.key == right_key:
                    self.player.move_right()
                    self.player.direction_moving = "right"

                elif event.key == left_key:
                    self.player.move_left()
                    self.player.direction_moving = "left"

                elif event.key == up_key:
                    self.player.move_up()
                    self.player.direction_moving = "up"

                elif event.key == down_key:
                    self.player.move_down()
                    self.player.direction_moving = "down"

            elif event.type == pygame.KEYUP:
                self.player.direction_moving = "still"
                if event.key == right_key:
                    self.player.stop_move_right()
                elif event.key == left_key:
                    self.player.stop_move_left()
                elif event.key == up_key:
                    self.player.stop_move_up()
                elif event.key == down_key:
                    self.player.stop_move_down()

        return False

    def run_logic(self, rand_num, sal_period, ghost_chase_level):
        self.sal_period = sal_period
        self.ghost_chase_level = ghost_chase_level

        if self.trial_over:
            grid, player_start_pos, ghosts_start_pos, dot_locs, grid_id, horizontal, vertical, intersection_2way, intersection_3way, intersection_4way = enviroment_setup(rand_num)
            all_points_info = horizontal + vertical + intersection_2way + intersection_3way + intersection_4way
            self.__init__(self.player_speed, grid, player_start_pos, ghosts_start_pos, dot_locs, grid_id, horizontal, vertical, intersection_2way, intersection_3way, intersection_4way, all_points_info)
            self.run_over = False
            self.trial_over = False

        else:
            self.player.update(self.horizontal_blocks, self.vertical_blocks, self.intersection_blocks, self.all_points_info)
            # When the block_hit_list contains one sprite that means that player hit a dot
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            if len(block_hit_list) > 0:
                eaten_dot = min(self.dot_locs, key=lambda c: (c[0]- self.player.rect.topleft[0])**2 + (c[1]-self.player.rect.topleft[1])**2)
                self.dot_locs = [x for x in self.dot_locs if x != eaten_dot]
                self.score += 1
                self.player.health += 20

            block_hit_list = pygame.sprite.spritecollide(self.player, self.ghosts, True)
            if len(block_hit_list) > 0: # caught by ghost
                self.player.explosion = True
                self.trial_over = True
                self.trial_end_reason = "killed"
                return True

            elif self.player.health <= 0: # health bar reached 0
                self.trial_over = True
                self.trial_end_reason = "starved"
                return True

            elif len(self.dot_locs) == 0: # consumed all dots
                self.trial_over = True
                self.trial_end_reason = "won"
                return True

            self.trial_over = self.player.trial_over
            self.ghosts.update(self.horizontal_blocks, self.vertical_blocks, self.intersection_blocks, self.player.rect.topleft, self.all_points_info, self.sal_period, self.ghost_chase_level)

        return False

    def display_frame(self, screen):
        screen.fill(BLACK)

        # draw the game here
        draw_enviroment(screen, self.grid)
        self.dots_group.draw(screen)
        self.ghosts.draw(screen)
        screen.blit(self.player.image, self.player.rect)
        # Render the text for the score
        text = self.font.render("Score: " + str(self.score), True, GREEN)
        # Put the text on the screen
        screen.blit(text, [120, 0])

        # display health bar
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH/2, 5, 100, 15))
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH/2, 5, self.player.health, 15))

        # update the screen with what has been drawn.
        pygame.display.flip()

    def log_information(self):
        info = {}
        ghost_locations = []
        ghost_distances_from_player = []
        dot_distances_from_player = []
        info["grid_ID"] = self.grid_id
        info["player_start_pos"] = self.player.start_pos
        info["player_loc"] = self.player.rect.topleft
        info["player_speed"] = self.player_speed

        for g in self.ghosts.sprites():
            ghost_locations.append(g.rect.topleft)
            ghost_dist_from_player = distance.cityblock(list(self.player.rect.topleft), list(g.rect.topleft))/36
            ghost_dist_from_player = int(round(ghost_dist_from_player, 0))
            ghost_distances_from_player.append(ghost_dist_from_player)

        for dot_loc in self.dot_locs:
            dot_dist_from_player = distance.cityblock(list(self.player.rect.topleft),list(dot_loc))/36
            dot_dist_from_player = int(round(dot_dist_from_player, 0))
            dot_distances_from_player.append(dot_dist_from_player)

        info["ghosts_locs"] = ghost_locations
        info["dots_locs"] = self.dot_locs
        info["ghosts_dists_from_player"] = ghost_distances_from_player
        info["dots_dists_from_player"] = dot_distances_from_player
        info["cum_ghosts_dist"] = sum(info["ghosts_dists_from_player"])
        info["salience_period"] = self.sal_period
        info["ghosts_chase_level"] = self.ghosts.sprites()[0].chase_level
        info["ghosts_speed"] = self.ghosts.sprites()[0].speed
        info["player_movement"] = self.player.direction_moving
        info["score"] = self.score
        info["health"] = self.player.health

        return info

