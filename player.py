import pygame
from config import *

class Player(pygame.sprite.Sprite):
    """Generates the player and all their aspects."""
    
    change_x = 0
    change_y = 0
    explosion = False
    trial_over = False

    def __init__(self, x, y, filename, player_speed):
        # call the parent class (sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.trial_over = False
        self.health = 100
        self.speed = player_speed
        self.upVal = 0
        self.downVal = 0
        self.leftVal = 0
        self.rightVal = 0
        img = pygame.image.load("walk.png").convert()

        # create the animations objects
        self.move_right_animation = Animation(img, 36, 36)
        self.move_left_animation = Animation(pygame.transform.flip(img, True, False), 36, 36)
        self.move_up_animation = Animation(pygame.transform.rotate(img, 90), 36, 36)
        self.move_down_animation = Animation(pygame.transform.rotate(img, 270), 36, 36)

        # load explosion image
        img = pygame.image.load("explosion.png").convert()
        self.explosion_animation = Animation(img, 36, 36)

        # save the player image
        self.player_image = pygame.image.load(filename).convert()
        self.player_image.set_colorkey(BLACK)


    def update(self, horizontal_blocks, vertical_blocks, intersection_blocks, all_points_info):

        allXY = [x[0] for x in all_points_info]

        # https://stackoverflow.com/questions/28339199/from-list-of-tuples-get-tuple-closest-to-a-given-value
        closest = min(allXY, key=lambda c: (c[0]- self.rect.topleft[0])**2 + (c[1]-self.rect.topleft[1])**2)
        self.closest = closest

        if self.rect.topleft in allXY:
            info = [x for x in all_points_info if self.rect.topleft in x][0] #always list of 1 list, so take first (i.e. only)
        else:
            info = [x for x in all_points_info if x[0] == self.closest][0]

        upVal, downVal, leftVal, rightVal = info[1]
        self.upVal = upVal
        self.downVal = downVal
        self.leftVal = leftVal
        self.rightVal = rightVal

        if not self.explosion:
            self.rect.x += self.change_x
            self.rect.y += self.change_y

#            self.health -= 0.05
            self.health -= 0.10

            # this will stop the player from moving through the blue lines
            for block in pygame.sprite.spritecollide(self, horizontal_blocks, False):
                self.rect.centery = block.rect.centery
                self.change_y = 0
            for block in pygame.sprite.spritecollide(self, vertical_blocks, False):
                self.rect.centerx = block.rect.centerx
                self.change_x = 0
            for block in pygame.sprite.spritecollide(self, intersection_blocks, False):
                if self.upVal == 0 and self.change_y < 0: #moving up but no longer allowed to
                    self.rect.centery = block.rect.centery
                    self.change_y = 0
                elif self.downVal == 0 and self.change_y > 0: # moving down but no longer allowed to
                    self.rect.centery = block.rect.centery
                    self.change_y = 0
                elif self.leftVal == 0 and self.change_x < 0: # moving left but no longer allowed to
                    self.rect.centerx = block.rect.centerx
                    self.change_x = 0
                elif self.rightVal == 0 and self.change_x > 0: # moving right but no longer allowed to
                    self.rect.centerx = block.rect.centerx
                    self.change_x = 0


            # this will cause the animation to start
            if self.change_x > 0:
                self.move_right_animation.update(10)
                self.image = self.move_right_animation.get_current_image()
            elif self.change_x < 0:
                self.move_left_animation.update(10)
                self.image = self.move_left_animation.get_current_image()

            if self.change_y > 0:
                self.move_down_animation.update(10)
                self.image = self.move_down_animation.get_current_image()
            elif self.change_y < 0:
                self.move_up_animation.update(10)
                self.image = self.move_up_animation.get_current_image()
        else:
            if self.explosion_animation.index == self.explosion_animation.get_length() -1:
                pygame.time.wait(100)
            self.explosion_animation.update(10)
            self.image = self.explosion_animation.get_current_image()
            self.trial_over = True

        return self


    def move_right(self):
        self.change_x = self.speed

    def move_left(self):
        self.change_x = -self.speed

    def move_up(self):
        self.change_y = -self.speed

    def move_down(self):
        self.change_y = self.speed

    def stop_move_right(self):
        if self.change_x != 0:
            self.image = self.player_image
        self.change_x = 0

    def stop_move_left(self):
        if self.change_x != 0:
            self.image = pygame.transform.flip(self.player_image, True, False)
        self.change_x = 0

    def stop_move_up(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image, 90)
        self.change_y = 0

    def stop_move_down(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image, 270)
        self.change_y = 0




class Animation(object):
    def __init__(self, img, width, height):
        # load the sprite sheet
        self.sprite_sheet = img
        # create a list to store the images
        self.image_list = []
        self.load_images(width, height)
        # create a variable which will hold the current image of the list
        self.index = 0
        # create a variable that will hold the time
        self.clock = 1

    def load_images(self, width, height):
        # go through every single image in the sprite sheet
        for y in range(0, self.sprite_sheet.get_height(), height):
            for x in range(0, self.sprite_sheet.get_width(), width):
                # load images into a list
                img = self.get_image(x, y, width, height)
                self.image_list.append(img)

    def get_image(self, x, y, width, height):
        # create a new blank image
        image = pygame.Surface([width, height]).convert()
        # copy the sprite from the large sheet onto the smaller
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # assuming black works as the transparent color
        image.set_colorkey((0, 0, 0))
        # return the image
        return image

    def get_current_image(self):
        return self.image_list[self.index]

    def get_length(self):
        return len(self.image_list)

    def update(self, fps=30):
        step = 30 // fps
        l = range(1, 30, step)
        if self.clock == 30:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in l:
            # increase index
            self.index += 1
            if self.index == len(self.image_list):
                self.index = 0




