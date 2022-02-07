import pygame
import random
from config import *
from scipy.spatial import distance


class Block(pygame.sprite.Sprite):
    """Information pertaining to the ghosts block shape."""
    
    def __init__(self, x, y, color, width, height):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Ellipse(pygame.sprite.Sprite):
    """Information pertaining to the Player ellipse shape."""
    
    def __init__(self, x, y, color, width, height):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        # draw the ellipse
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class ghost(pygame.sprite.Sprite):
    "Generating the ghosts and all their aspects."""
    
    def __init__(self, x, y, change_x, change_y, player_speed):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.change_x = change_x
        self.change_y = change_y
        self.image = pygame.image.load("ghosts_threat.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = "NA"
        self.chase_level = 20
        self.speed_options = [player_speed-0.3, player_speed, player_speed+1]
        self.speed = player_speed
        self.distance_from_player = 1000
        self.best_chase_dir = ""
        self.previous_best_chase_dir = ""
        self.previous_best_chase_dir_flip = ""

    def update(self, horizontal_blocks, vertical_blocks, intersection_blocks, player_loc, all_points_info, sal_period, chase_level):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        self.sal_period = sal_period
        self.chase_level = chase_level

        self.distance_from_player = distance.cityblock(list(self.rect.topleft), list(player_loc))

        # load ghost image based on salience condition period
        if self.sal_period == "safe":
            self.image = pygame.image.load("ghosts_safe.png").convert_alpha()
        else:
            self.image = pygame.image.load("ghosts_threat.png").convert_alpha()

        if self.rect.topleft in [x[0] for x in all_points_info]:
            info = [x for x in all_points_info if self.rect.topleft in x][0] #always list of 1 list, so take first (i.e. only)
            upVal, downVal, leftVal, rightVal = info[1]
            legal_directions = info[2]
            pos_type = info[3]

            # tracking/chasing info for ghosts
            if pos_type in ["2way", "3way", "4way"]:
                if self.sal_period == "threat":
                    self.speed = random.choice(self.speed_options)
                else:
                    self.speed = random.choice(self.speed_options[:2]) # don't let ghosts be faster than player during safe period

                chase_options = {}
                for legal_dir in legal_directions:
                    if legal_dir == "up":
                        new_pos_loc = tuple(map(lambda i, j: i - j, self.rect.topleft, (0, 32)))
                    elif legal_dir == "down":
                        new_pos_loc = tuple(map(lambda i, j: i + j, self.rect.topleft, (0, 32)))
                    elif legal_dir == "right":
                        new_pos_loc = tuple(map(lambda i, j: i + j, self.rect.topleft, (32, 0)))
                    elif legal_dir == "left":
                        new_pos_loc = tuple(map(lambda i, j: i - j, self.rect.topleft, (32, 0)))

                    new_dist = distance.cityblock(list(new_pos_loc), list(player_loc))
                    chase_options[legal_dir] = new_dist

                min_dist = min(chase_options.items(), key=lambda x : x[1])[1]
                min_dist_directions = [key for (key, value) in chase_options.items() if value == min_dist]

                if len(min_dist_directions) == 1:
                    self.best_chase_dir = min_dist_directions[0]
                else:
                    self.best_chase_dir = [x for x in min_dist_directions if x != self.previous_best_chase_dir_flip][0]

                self.previous_best_chase_dir = self.best_chase_dir
                if self.previous_best_chase_dir == "up":
                    self.previous_best_chase_dir_flip = "down"
                elif self.previous_best_chase_dir == "down":
                    self.previous_best_chase_dir_flip = "up"
                elif self.previous_best_chase_dir == "left":
                    self.previous_best_chase_dir_flip = "right"
                elif self.previous_best_chase_dir == "right":
                    self.previous_best_chase_dir_flip = "left"

                if random.choice([x for x in range(1, 101)]) <= self.chase_level:
                    self.direction = self.best_chase_dir
                else:
                    self.direction = random.choice([x for x in legal_directions if x != self.best_chase_dir])
            else: # check that horizontal/vertical movement is proper
                if pos_type == "horizontal":
                    if self.change_x == -self.speed: # already moving left, so keep it that way
                        self.direction = "left"
                    elif self.change_x == self.speed: # already moving right, so keep it that way
                        self.direction = "right"
                elif pos_type == "vertical":
                    if self.change_y == -self.speed: # already moving up, so keep it that way
                        self.direction = "up"
                    elif self.change_y == self.speed: # already moving down, so keep it that way
                        self.direction = "down"

        # apply direction and speed changes once ghost reaches intersection
        if self.direction == "left":
            self.change_x = -self.speed
            self.change_y = 0
        elif self.direction == "right":
            self.change_x = self.speed
            self.change_y = 0
        elif self.direction == "up":
            self.change_x = 0
            self.change_y = -self.speed
        elif self.direction == "down":
            self.change_x = 0
            self.change_y = self.speed

        return self